import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

export default function ArticleCard({title}:{title:string}){
    return(
        <Card sx={{width:300}}>
            <CardContent>
                <Typography gutterBottom sx={{ color: 'text.primary', fontSize: 30 }}>
                    {title}
                </Typography>
            </CardContent>
            <CardActions>
                <Button size="large">AIで要約</Button>
            </CardActions>
        </Card>
    )
    
}