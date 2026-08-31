import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { useState } from 'react';

export default function ArticleCard({title}:{title:string}){
    const [isOpen,setIsOpen] = useState(false)
    const summary = "要約部分"
    const handleIsOpen = () => {
        setIsOpen(!isOpen)
    }
    return(
        <Card sx={{width:300}}>
            <CardContent>
                <Typography gutterBottom sx={{ color: 'text.primary', fontSize: 30 }}>
                    {title}
                </Typography>
            </CardContent>
            <CardActions>
                <Button size="large" onClick={handleIsOpen}>AIで要約</Button>
            </CardActions>
            <CardContent>
                {isOpen && summary}
            </CardContent>
        </Card>
    )
    
}