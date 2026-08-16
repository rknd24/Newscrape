import Button from '@mui/material/Button'
import Typography from '@mui/material/Typography'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CardActions from '@mui/material/CardActions'

export default function ArticleCard({title}:{title:string}){
    return (
    <Card sx={{ width: 355 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ color: 'text.primary' }}>
          {title}
          </Typography>
        </CardContent>
        <CardActions>
          <Button>AIで要約</Button>
        </CardActions>
    </Card>
    )
}