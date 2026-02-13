// import { FileText, ArrowRight } from 'lucide-react'

// export default function HomePage() {
//   return (
//     <div className="min-h-[calc(100vh-4rem)] flex flex-col">
//       <section className="flex-1 flex flex-col items-center justify-center px-4 py-20">
//         <div className="text-center max-w-2xl mx-auto">
//           <div className="mb-6">
//             <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-forest/10 mb-6">
//               <FileText className="w-10 h-10 text-forest" />
//             </div>
//           </div>

//           <h1 className="text-4xl sm:text-5xl font-bold text-dark mb-4 leading-tight">
//             دانشنامه (ویکی)
//           </h1>
//           <p className="text-gray-600 text-lg">
//             به دانشنامه گروه ۲ خوش آمدید. از منوی بالا برای جستجو، ایجاد و مدیریت مقالات استفاده کنید.
//           </p>
//         </div>
//       </section>

//       <footer className="border-t border-gray-300 py-6 text-center">
//         <a
//           href="http://localhost:8000"
//           className="inline-flex items-center gap-2 text-gray-500 hover:text-forest transition-colors text-sm"
//         >
//           <ArrowRight className="w-4 h-4" />
//           بازگشت به داشبورد اصلی
//         </a>
//       </footer>
//     </div>
//   )
// }
import { useEffect, useState } from "react"
import { FileText, ArrowRight } from "lucide-react"

export default function HomePage() {
  const [topArticles, setTopArticles] = useState([])
  const [recentArticles, setRecentArticles] = useState([])
  const [popularTags, setPopularTags] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        // --- TOP ---
        try {
          const r1 = await fetch("http://localhost:9106/api/articles/top/?limit=5")
          if (r1.ok) setTopArticles(await r1.json())
          else setTopArticles([])
        } catch {
          setTopArticles([])
        }

        // --- RECENT ---
        try {
          const r2 = await fetch("http://localhost:9106/api/articles/recent/?limit=5")
          if (r2.ok) setRecentArticles(await r2.json())
          else setRecentArticles([])
        } catch {
          setRecentArticles([])
        }

        // --- TAGS ---
        try {
          const r3 = await fetch("http://localhost:9106/api/tags/popular/?limit=5")
          if (r3.ok) setPopularTags(await r3.json())
          else setPopularTags([])
        } catch {
          setPopularTags([])
        }

      } finally {
        setLoading(false)
      }
    }

    load()
  }, [])

  if (loading)
    return <div className="p-10 text-center text-gray-500">در حال بارگذاری...</div>

  return (
    <div className="min-h-screen flex flex-col px-4 py-10">

      {/* HEADER */}
      <header className="text-center mb-14">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-forest/10 mx-auto mb-4">
          <FileText className="w-10 h-10 text-forest" />
        </div>
        <h1 className="text-4xl sm:text-5xl font-bold text-dark mb-2">
          دانشنامه گروه ۲
        </h1>
      </header>


      {/* CONTENT (ONLY THIS IS GRID) */}
      <main className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto w-full flex-1">

        {/* TOP ARTICLES */}
        <section className="bg-white rounded-xl border p-5 shadow-sm">
          <h2 className="text-xl font-semibold mb-4 text-center">برترین مقالات</h2>
          <ul className="space-y-2">
            {topArticles.length === 0 ? (
              <p className="text-gray-400 text-center">موردی یافت نشد</p>
            ) : (
              topArticles.map(article => (
                <li key={article.name} className="p-3 rounded-lg hover:bg-gray-50 transition">
                  {article.name} — امتیاز: {article.score ?? 0}
                </li>
              ))
            )}
          </ul>
        </section>


        {/* RECENT ARTICLES */}
        <section className="bg-white rounded-xl border p-5 shadow-sm">
          <h2 className="text-xl font-semibold mb-4 text-center">جدیدترین مقالات</h2>
          <ul className="space-y-2">
            {recentArticles.length === 0 ? (
              <p className="text-gray-400 text-center">موردی یافت نشد</p>
            ) : (
              recentArticles.map(article => (
                <li key={article.name} className="p-3 rounded-lg hover:bg-gray-50 transition">
                  {article.name} —{" "}
                  {article.created_at
                    ? new Date(article.created_at).toLocaleDateString()
                    : "—"}
                </li>
              ))
            )}
          </ul>
        </section>


        {/* POPULAR TAGS */}
        <section className="bg-white rounded-xl border p-5 shadow-sm">
          <h2 className="text-xl font-semibold mb-4 text-center">تگ‌های محبوب</h2>
          <div className="flex flex-wrap gap-2 justify-center">
            {popularTags.length === 0 ? (
              <p className="text-gray-400 text-center">تگی وجود ندارد</p>
            ) : (
              popularTags.map(tag => (
                <span
                  key={tag.name}
                  className="px-3 py-1 bg-forest/10 rounded-full text-forest font-medium"
                >
                  {tag.name} ({tag.score ?? 0})
                </span>
              ))
            )}
          </div>
        </section>

      </main>


      {/* FOOTER (ALWAYS BOTTOM) */}
      <footer className="border-t border-gray-300 py-6 text-center mt-14">
        <a
          href="http://localhost:8000"
          className="inline-flex items-center gap-2 text-gray-500 hover:text-forest transition-colors text-sm"
        >
          <ArrowRight className="w-4 h-4" />
          بازگشت به داشبورد اصلی
        </a>
      </footer>
    </div>
  )
}
