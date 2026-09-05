import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CardActions from '@mui/material/CardActions'
import Button from '@mui/material/Button'
import Link from '@mui/material/Link'
import Collapse from '@mui/material/Collapse'
import Typography from '@mui/material/Typography'
import { useState } from 'react'
import ReactMarkdown from "react-markdown"
import { analyze } from '../api'
import type { Article } from '../api'
import { formatRelativeTime } from '../formatRelativeTime'

type State = "idle" | "loading" | "success" | "error"

export default function ArticleCard({ article }: { article: Article }) {
    const [open, setOpen] = useState(false)
    const [summary, setSummary] = useState(article.summary ?? "")
    const [state, setState] = useState<State>(article.summary ? "success" : "idle")

    const handleToggle = () => {
        setOpen(!open)
        // 事前生成された要約が無ければ、開くタイミングでその場生成
        if (!open && !summary && (state === "idle" || state === "error")) {
            setState("loading")
            analyze(article)
                .then(data => {
                    setSummary(data.report)
                    setState("success")
                })
                .catch(() => setState("error"))
        }
    }

    return (
        <Card sx={{ width: { xs: "100%", sm: 340 }, display: "flex", flexDirection: "column" }}>
            <CardContent sx={{ flexGrow: 1 }}>
                <Typography sx={{ fontSize: 18, fontWeight: 600, lineHeight: 1.4 }}>
                    {article.title}
                </Typography>
                <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: "block" }}>
                    {formatRelativeTime(article.fetched_at)}
                </Typography>
            </CardContent>
            <CardActions sx={{ justifyContent: "space-between" }}>
                <Button size="small" onClick={handleToggle}>
                    {open ? "閉じる" : "要約"}
                </Button>
                <Link href={article.link} target="_blank" rel="noopener" variant="body2">
                    元記事
                </Link>
            </CardActions>
            <Collapse in={open} unmountOnExit>
                <CardContent sx={{ pt: 0 }}>
                    {state === "loading" && <Typography variant="body2">要約を生成中…</Typography>}
                    {state === "error" && (
                        <Typography variant="body2" color="error">
                            要約の取得に失敗しました。
                        </Typography>
                    )}
                    {state === "success" && (
                        <Typography variant="body2" component="div">
                            <ReactMarkdown>{summary}</ReactMarkdown>
                        </Typography>
                    )}
                </CardContent>
            </Collapse>
        </Card>
    )
}
