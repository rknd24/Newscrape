import { chat,type ChatMessage } from '../api'
import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Paper from '@mui/material/Paper'
import TextField from '@mui/material/TextField'
import IconButton from '@mui/material/IconButton'
import CircularProgress from '@mui/material/CircularProgress'
import Typography from '@mui/material/Typography'
import SendIcon from '@mui/icons-material/Send'

type ChatProps = {
    articleId: number
}

export default function Chat({ articleId }: ChatProps) {
    const [question, setQuestion] = useState("")
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [history, setHistory] = useState<ChatMessage[]>([])

    const handleSend = () => {
        const text = question.trim()
        if(!text || loading){
            return 
        }

        const preHistory = history
        setHistory(prev => [...prev, { role: 'user', content: text }])
        setQuestion("")
        setLoading(true)
        setError(null)

        chat(text, articleId, preHistory)
            .then(data => {
                setHistory(prev => [...prev, { role: 'assistant', content: data.answer }])
            })
            .catch(() => {
                setError("質問の送信に失敗しました。")
            })
            .finally(() => {
                setLoading(false)
            })
    }

    return (
        <Box sx={{ display: "flex", flexDirection: "column", height: "100%" }}>
            <Stack spacing={1} sx={{flex: 1, overflowY: "auto", p:2}}>
                {history.map((msg,index) => (
                    <Paper
                        key = {index}
                        elevation={0}
                        sx={{
                            alignSelf: msg.role === 'user' ? "flex-end" : "flex-start",
                            maxWidth: "85%",
                            px: 1.5,
                            py: 1,
                            borderRadius: 2,
                            bgcolor: msg.role === 'user' ? "primary.main" : "grey.100",
                            color: msg.role === 'user' ? "primary.contrastText" : "text.primary",
                            fontSize: 14,
                            lineHeight: 1.7,
                            whiteSpace: msg.role === 'user' ? "pre-wrap" : "normal",
                            // assistant の回答は Markdown で描画する。段落の余白を詰める
                            "& p": { m: 0 },
                            "& p + p": { mt: 1 },
                            "& ul, & ol": { my: 0, pl: 2.5 },
                        }}
                    >
                        {msg.role === 'assistant'
                            ? <ReactMarkdown>{msg.content}</ReactMarkdown>
                            : msg.content}
                    </Paper>
                ))}
            </Stack>

            {loading && (
                <Box sx={{ px:2, py: 1 }}>
                    <CircularProgress size={16} />
                </Box>
            )}

            {error && (
                <Typography color="error" sx={{ px: 2, py: 1, fontSize: 14 }}>
                    {error}
                </Typography>
            )}

            <Box
                component="form"
                onSubmit={(e) => { e.preventDefault(); handleSend() }}
                sx={{ display: "flex", gap: 1, p: 2, borderTop: 1, borderColor: "divider" }}
            >
                <TextField
                    fullWidth
                    size="small"
                    placeholder="質問を入力"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                />
                <IconButton
                    type="submit"
                    color="primary"
                    disabled={loading || !question.trim()}
                >
                    <SendIcon />
                </IconButton>
            </Box>
        </Box>
    )
}


    