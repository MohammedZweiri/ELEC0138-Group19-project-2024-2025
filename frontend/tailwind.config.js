/** @type {import('tailwindcss').Config} */
export default {
    content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}",],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                primary: {
                    50: '#f5f3ff',
                    100: '#ede9fe',
                    200: '#ddd6fe',
                    300: '#c4b5fd',
                    400: '#a78bfa',
                    500: '#8b5cf6',
                    600: '#7c3aed',
                    700: '#6d28d9',
                    800: '#5b21b6',
                    900: '#4c1d95',
                    950: '#2e1065',
                },
            }, fontFamily: {
                sans: ['Inter', 'sans-serif'],
            }, borderRadius: {
                'xl': '0.75rem', '2xl': '1rem', '3xl': '1.5rem',
            }, boxShadow: {
                'subtle': '0 2px 5px 0 rgba(0,0,0,0.05)', 'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.15)',
            }, animation: {
                'fade-in': 'fadeIn 0.5s ease-out',
            }, keyframes: {
                fadeIn: {
                    '0%': {opacity: '0'}, '100%': {opacity: '1'},
                },
            },
        },
    },
    plugins: [require('@tailwindcss/typography'), require('@tailwindcss/forms'), require('@tailwindcss/aspect-ratio'),],
}