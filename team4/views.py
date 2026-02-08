from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist
from .fields import Point

from core.auth import api_login_required
from team4.models import Facility, Category, City, Amenity
from team4.serializers import (
    FacilityListSerializer, FacilityDetailSerializer,
    FacilityNearbySerializer, FacilityComparisonSerializer,
    CategorySerializer, CitySerializer, AmenitySerializer,
    FacilityCreateSerializer
)
from team4.services.facility_service import FacilityService

TEAM_NAME = "team4"


# =====================================================
# Pagination
# =====================================================
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# =====================================================
# ViewSets
# =====================================================

class FacilityViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای مدیریت امکانات
    
    APIs:
    - GET /api/facilities/              → لیست امکانات با جستجو و فیلتر
    - GET /api/facilities/{id}/         → جزئیات یک مکان
    - GET /api/facilities/{id}/nearby/  → امکانات نزدیک
    - POST /api/facilities/compare/     → مقایسه هتل‌ها
    """
    queryset = Facility.objects.filter(status=True)
    pagination_class = StandardResultsSetPagination
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FacilityListSerializer
        elif self.action == 'retrieve':
            return FacilityDetailSerializer
        elif self.action == 'create':
            return FacilityCreateSerializer
        return FacilityDetailSerializer
    
    def list(self, request):
        # دریافت پارامترها
        city_name = request.query_params.get('city')
        category_name = request.query_params.get('category')
        sort_by = request.query_params.get('sort', 'rating')
        
        # جستجو
        facilities = FacilityService.search_facilities(
            city_name=city_name,
            category_name=category_name
        )
        
        # فیلتر
        filters = {
            'min_price': request.query_params.get('min_price'),
            'max_price': request.query_params.get('max_price'),
            'min_rating': request.query_params.get('min_rating'),
            'amenities': request.query_params.get('amenities'),
            'is_24_hour': request.query_params.get('is_24_hour'),
        }
        
        # حذف فیلترهای None
        filters = {k: v for k, v in filters.items() if v is not None}
        
        if filters:
            facilities = FacilityService.filter_facilities(facilities, filters)
        
        # مرتب‌سازی
        if sort_by == 'rating':
            facilities = facilities.order_by('-avg_rating', '-review_count')
        elif sort_by == 'review_count':
            facilities = facilities.order_by('-review_count')
        elif sort_by == 'distance' and city_name:
            # برای مرتب‌سازی بر اساس فاصله، نیاز به مرکز شهر داریم
            try:
                city = City.objects.filter(
                    name_fa__icontains=city_name
                ).first() or City.objects.filter(
                    name_en__icontains=city_name
                ).first()
                
                if city and city.location:
                    facilities_list = list(facilities)
                    sorted_facilities = FacilityService.sort_by_distance(
                        facilities_list,
                        city.location
                    )
                    
                    # استفاده از pagination
                    page = self.paginate_queryset([f['facility'] for f in sorted_facilities])
                    if page is not None:
                        serializer = self.get_serializer(page, many=True)
                        return self.get_paginated_response(serializer.data)
                    
                    serializer = self.get_serializer(
                        [f['facility'] for f in sorted_facilities],
                        many=True
                    )
                    return Response(serializer.data)
            except:
                pass
        
        # Pagination
        page = self.paginate_queryset(facilities)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(facilities, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            facility = FacilityService.get_facility_details(pk)
            serializer = self.get_serializer(facility)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(
                {'error': f'مکان با شناسه {pk} یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def nearby(self, request, pk=None):
        radius = float(request.query_params.get('radius', 5))
        category_name = request.query_params.get('category')
        
        nearby_facilities = FacilityService.get_nearby_facilities(
            fac_id=pk,
            radius_km=radius,
            category_name=category_name
        )
        
        if not nearby_facilities:
            return Response(
                {'message': 'هیچ امکاناتی در این شعاع یافت نشد'},
                status=status.HTTP_200_OK
            )
        
        # دریافت مکان مرکزی
        try:
            center_facility = Facility.objects.get(fac_id=pk)
            center_data = FacilityListSerializer(center_facility).data
        except Facility.DoesNotExist:
            return Response(
                {'error': 'مکان مرجع یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = FacilityNearbySerializer(nearby_facilities, many=True)
        
        return Response({
            'center': center_data,
            'radius_km': radius,
            'count': len(nearby_facilities),
            'nearby_facilities': serializer.data
        })
    
    @action(detail=False, methods=['post'])
    def compare(self, request):
        """
        FR-8: مقایسه هتل‌ها
        
        Body:
            {
                "facility_ids": [123, 125, 130]
            }
        """
        facility_ids = request.data.get('facility_ids', [])
        
        if not facility_ids:
            return Response(
                {'error': 'لیست facility_ids الزامی است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        comparison = FacilityService.compare_facilities(facility_ids)
        
        if 'error' in comparison:
            return Response(comparison, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(comparison)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.select_related('province').all()
    serializer_class = CitySerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        province = self.request.query_params.get('province')
        
        if province:
            queryset = queryset.filter(province__name_fa__icontains=province)
        
        return queryset


class AmenityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer


@api_login_required
def ping(request):
    return JsonResponse({"team": TEAM_NAME, "ok": True})


def base(request):
    return render(request, f"{TEAM_NAME}/index.html")