// // // /** @type {import('tailwindcss').Config} */
// // // module.exports = {
// // //   content: [
// // //     './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
// // //     './src/components/**/*.{js,ts,jsx,tsx,mdx}',
// // //     './src/app/**/*.{js,ts,jsx,tsx,mdx}',
// // //   ],
// // //   theme: {
// // //     extend: {
// // //       colors: {
// // //         primary: {
// // //           50: '#f0f9ff',
// // //           100: '#e0f2fe',
// // //           200: '#bae6fd',
// // //           300: '#7dd3fc',
// // //           400: '#38bdf8',
// // //           500: '#0ea5e9',
// // //           600: '#0284c7',
// // //           700: '#0369a1',
// // //           800: '#075985',
// // //           900: '#0c4a6e',
// // //         },
// // //       },
// // //     },
// // //   },
// // //   plugins: [],
// // // }












// // /** @type {import('tailwindcss').Config} */
// // module.exports = {
// //   content: [
// //     './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
// //     './src/components/**/*.{js,ts,jsx,tsx,mdx}',
// //     './src/app/**/*.{js,ts,jsx,tsx,mdx}',
// //   ],
// //   theme: {
// //     extend: {
// //       colors: {
// //         primary: {
// //           50: '#f0f9ff',
// //           100: '#e0f2fe',
// //           200: '#bae6fd',
// //           300: '#7dd3fc',
// //           400: '#38bdf8',
// //           500: '#0ea5e9',
// //           600: '#0284c7',
// //           700: '#0369a1',
// //           800: '#075985',
// //           900: '#0c4a6e',
// //         },
// //         border: '#E5E7EB', // ✅ Add this
// //       },
// //     },
// //   },
// //   plugins: [],
// // }



















// /** @type {import('tailwindcss').Config} */
// module.exports = {
//   content: [
//     './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
//     './src/components/**/*.{js,ts,jsx,tsx,mdx}',
//     './src/app/**/*.{js,ts,jsx,tsx,mdx}',
//   ],
//   theme: {
//     extend: {
//       colors: {
//         primary: {
//           50: '#f0f9ff',
//           100: '#e0f2fe',
//           200: '#bae6fd',
//           300: '#7dd3fc',
//           400: '#38bdf8',
//           500: '#0ea5e9',
//           600: '#0284c7',
//           700: '#0369a1',
//           800: '#075985',
//           900: '#0c4a6e',
//         },
//         border: '#E5E7EB',     // previous fix
//         background: '#F9FAFB', // ✅ add this for bg-background
//       },
//     },
//   },
//   plugins: [],
// }
















/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        border: '#E5E7EB',         // border-border
        background: '#F9FAFB',     // bg-background
        foreground: '#111827',     // text-foreground
      },
    },
  },
  plugins: [],
}
