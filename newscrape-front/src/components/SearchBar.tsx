import { useState } from "react"
import Box from '@mui/material/Box'
import TextField from '@mui/material/TextField'
import IconButton from '@mui/material/IconButton'
import InputAdornment from '@mui/material/InputAdornment'

export default function Search_Bar({ onSearch }: { onSearch: (word: string) => void }) {
    const [word, setWord] = useState("")

    const handleClear = () => {
        setWord("")
        onSearch("")
    }

    return (
        <Box
            component="form"
            onSubmit={(e) => { e.preventDefault(); onSearch(word) }}
        >
            <TextField
                label="キーワード検索"
                size="small"
                fullWidth
                value={word}
                onChange={(e) => setWord(e.target.value)}
                slotProps={{
                    input: {
                        endAdornment: word && (
                            <InputAdornment position="end">
                                <IconButton
                                    size="small"
                                    onClick={handleClear}
                                    edge="end"
                                    aria-label="検索語をクリア"
                                    sx={{ fontSize: '1.1rem', lineHeight: 1 }}
                                >
                                    ×
                                </IconButton>
                            </InputAdornment>
                        ),
                    },
                }}
            />
        </Box>
    )
}
