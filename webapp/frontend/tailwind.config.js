/** @type {import('tailwindcss').Config} */
export default {
    darkMode: ["class"],
    content: ["./index.html", "./src/**/*.{ts,tsx,js,jsx}"],
  theme: {
  	extend: {
  		borderRadius: {
  			lg: 'var(--radius)',
  			md: 'calc(var(--radius) - 2px)',
  			sm: 'calc(var(--radius) - 4px)'
  		},
  		colors: {},
  		keyframes: {
  			'slide-down': {
  				'0%': { transform: 'translateY(-100%)', opacity: '0' },
  				'100%': { transform: 'translateY(0)', opacity: '1' },
  			}
  		},
  		animation: {
  			'slide-down': 'slide-down 0.3s ease-out',
  		}
  	}
  },
  plugins: [import("tailwindcss-animate")],
}

