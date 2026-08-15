import Button from '@mui/material/Button'
import Typography from '@mui/material/Typography'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CardActions from "@mui/material/CardActions"




function App() {
  return (
    <Card sx={{ width: 355 }}>
        <CardContent>
          <Typography gutterBottom sx={{ color: 'text.primery', fontSize: 36 }}>
          仮の記事タイトル
          </Typography>
        </CardContent>
        <CardActions>
          <Button>AIで要約</Button>
        </CardActions>
    </Card>

        
      
  )
}

export default App
