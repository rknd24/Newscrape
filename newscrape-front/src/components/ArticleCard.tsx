import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { useState } from 'react';
import ReactMarkdown from "react-markdown"
import { analyze } from '../api';
import type { Article } from '../api';
export default function ArticleCard({article}:{article:Article}){
    const [summary,setSummary] = useState("")
    type State = "idle" | "loading" | "success" | "error"
    const [state,setState] = useState<State>("idle")
    const handleSummarize= () => {
        if(state == "idle" || state == "error"){
            setState("loading")
            analyze(article).then(data => {
                setState("success")
                setSummary(data.report)
            })
            .catch(() => {
                    setState("error")
                }
            )
        }
    }
    
    return(
        <Card sx={{width:300}}>
            <CardContent>
                <Typography gutterBottom sx={{ color: 'text.primary', fontSize: 30 }}>
                    {article.title}
                </Typography>
            </CardContent>
            <CardActions>
                <Button size="large" onClick={handleSummarize}>AIで要約</Button>
            </CardActions>
            <CardContent>
                {state == "loading" && <p>loading…</p>}
                {state == "success" && <ReactMarkdown>{summary}</ReactMarkdown>}
                {state == "error" && <p>記事取得に失敗しました。</p>}
            </CardContent>
        </Card>
    )
    
}