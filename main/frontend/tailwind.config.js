export default {
  content: ['./index.html', './**/*.{vue,ts}', '!./node_modules/**', '!./dist/**'],
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        success: '#10B981',
        warning: '#F59E0B',
        danger: '#EF4444'
      },
      scale: {
        '102': '1.02'
      }
    }
  },
  plugins: []
}
