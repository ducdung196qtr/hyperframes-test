const DURATION = 11.9;
const tl = gsap.timeline({ paused: true });

gsap.set([s1,s2,s3,s4,s5,s6], { opacity: 0, scale: 1.04 });

// Scene 1: 0.00s → 2.27s (2.27s)
tl.to(s1, { opacity: 1, scale: 1, duration: 0.4, ease: 'power2.out' }, 0.00)
  .to(s1, { opacity: 0, scale: 1.04, duration: 0.3, ease: 'power3.in' }, 1.97)

// Scene 2: 2.71s → 4.92s (2.21s)
tl.to(s2, { opacity: 1, scale: 1, duration: 0.4, ease: 'power2.out' }, 2.71)
  .to(s2, { keyframes: [{x:-6,dur:0.04},{x:6,dur:0.04},{x:-4,dur:0.04},{x:4,dur:0.04},{x:0,dur:0.04}] }, 3.71)
  .to(s2, { opacity: 0, scale: 1.04, duration: 0.3, ease: 'power3.in' }, 4.62)

// Scene 3: 5.39s → 6.97s (1.58s)
tl.to(s3, { opacity: 1, scale: 0.88, duration: 0.04 }, 5.39)
  .to(s3, { opacity: 1, scale: 1, duration: 0.45, ease: 'back.out(3)' }, 5.49)
  .to(s3, { opacity: 0, scale: 1.04, duration: 0.3, ease: 'power3.in' }, 6.67)

// Scene 4: 6.77s → 7.84s (1.07s)
tl.to(s4, { opacity: 1, scale: 0.9, duration: 0.04 }, 6.77)
  .to(s4, { opacity: 1, scale: 1, duration: 0.5, ease: 'back.out(2.5)' }, 6.87)
  .to(s4, { opacity: 0, scale: 1.04, duration: 0.3, ease: 'power3.in' }, 7.54)

// Scene 5: 8.41s → 11.01s (2.60s)
tl.to(s5, { opacity: 1, scale: 1, duration: 0.4, ease: 'power2.out' }, 8.41)
  .to(s5, { opacity: 0, scale: 1.04, duration: 0.3, ease: 'power3.in' }, 10.71)

// Scene 6: 11.45s → 11.88s (0.43s)
tl.to(s6, { opacity: 1, scale: 1, duration: 0.4, ease: 'power2.out' }, 11.45)

// Final scene stays visible
window.__timelines = { 'main': tl };
window.seekTo = function(t) { tl.progress(Math.min(t / DURATION, 1.0)); };
