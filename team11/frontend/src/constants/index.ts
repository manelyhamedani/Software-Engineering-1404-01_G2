const shuffle = (array: string[]) => array.sort(() => Math.random() - 0.5);

const rawImages = [
  '/team11/images/baz1.jpg', '/team11/images/baz2.jpg', '/team11/images/baz3.jpg', '/team11/images/baz4.jpg', '/team11/images/baz5.jpg',
  '/team11/images/his1.jpg', '/team11/images/his2.jpg', '/team11/images/his3.jpg', '/team11/images/his4.jpg', '/team11/images/his5.jpg',
  '/team11/images/his6.jpg', '/team11/images/his7.jpg', '/team11/images/his8.jpg', '/team11/images/his9.jpg', '/team11/images/his10.jpg',
  '/team11/images/his11.jpg', '/team11/images/his12.jpg', '/team11/images/his13.jpg', '/team11/images/his14.jpg',
  '/team11/images/maz1.jpg', '/team11/images/maz2.jpg', '/team11/images/maz3.jpg',
  '/team11/images/nat1.jpg', '/team11/images/nat2.jpg', '/team11/images/nat3.jpg', '/team11/images/nat4.jpg', '/team11/images/nat5.jpg',
  '/team11/images/nat6.jpg', '/team11/images/nat7.jpg', '/team11/images/nat9.jpg', '/team11/images/nat10.jpg',
  '/team11/images/rod1.jpg', '/team11/images/rod2.jpg', '/team11/images/rod3.jpg', '/team11/images/rod4.jpg', '/team11/images/rod5.jpg',
  '/team11/images/sea1.jpg', '/team11/images/sea2.jpg', '/team11/images/sea3.jpg', '/team11/images/sea4.jpg'
];

export const SCROLLING_IMAGES = shuffle([...rawImages]);