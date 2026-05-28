module.exports = {
  content: ["./templates/**/*.html", "./blog/**/*.py", "./profiles/**/*.py"],
  theme: {
    extend: {
      colors: {
        paper: "#f7f4ee",
        ink: "#171716",
        sage: "#61735f",
        clay: "#9a6249"
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        serif: ["Noto Serif KR", "Georgia", "serif"]
      }
    }
  },
  plugins: []
};
