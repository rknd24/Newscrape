import ArticleList from "./components/ArticleList"
import Logo from "./components/Logo"
import CssBaseline from '@mui/material/CssBaseline'
import Container from '@mui/material/Container'
import { ThemeProvider } from '@mui/material/styles'
import theme from './theme'

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg" sx={{ py: 3, px: { xs: 2, sm: 3 } }}>
        <Logo />
        <ArticleList />
      </Container>
    </ThemeProvider>
  )
}
