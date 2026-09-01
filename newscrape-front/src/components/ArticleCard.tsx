import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { useState } from 'react';

export default function ArticleCard({title,link}:{title:string,link:string}){
    const [Summary,setSummary] = useState("")
    const handleIsOpen = () => {
        if(state == "idle" || state == "error"){
            setState("loading")
            fetch("/analyze",{
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({title:title,link:link})
            }).then(res => res.json().then(data => ({ok:res.ok,data})))
            .then(({ok,data}) => {
                if (ok) {
                    setState("success")
                    setSummary(data.report)
                } else {
                    setState("error")
                }
            })
        }
    }
    const [state,setState] = useState("idle")
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
                {state == "loading" && <p>loading…</p>}
                {state == "success" && <p>{Summary}</p>}
                {state == "error" && <p>error</p>}
            </CardContent>
        </Card>
    )
    
}