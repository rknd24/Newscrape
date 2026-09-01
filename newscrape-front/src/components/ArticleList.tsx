import ArticleCard from "./ArticleCard"
import { useState } from "react"
import { useEffect } from "react"
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { type SelectChangeEvent } from '@mui/material/Select';

interface Article {
    title: string;
    link: string;
}

type Status = "idle" | "loading" | "success" | "error"

export default function ArticleList(){
    const [articleData,setArticleData] = useState<Article[]>([])
    const [category,setCategory] = useState("1")
    const [state,setState] = useState<Status>("idle")
    useEffect(() => {
        setState("loading")
        fetch(`/news/${category}`).then(res => res.json().then(data => ({ok:res.ok,data})))
        .then(({ok,data}) => {
            if(ok){
                setArticleData(data.articles);
                setState("success")
            } else {
                setState("error")
            }
            
        })
        .catch(() => {
            setState("error")
        })
    },[category])
     const handleChange = (event: SelectChangeEvent) => {
        setCategory(event.target.value as string);
    };
    return(
        <div>
            {state == "loading" && <p>NowLoading…</p>}
            {state == "error" && <p>読み込みに失敗しました。</p>}
            <FormControl sx={{ minWidth: 200, mb: 3 }}>
                <InputLabel id="demo-simple-select-label">category</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={category}
                    label="Category"
                    onChange={handleChange}
                >
                <MenuItem value="1">総合</MenuItem>
                <MenuItem value="2">経済</MenuItem>
                <MenuItem value="3">IT</MenuItem>
                </Select>
            </FormControl>
            <Box sx={{display:"flex",flexWrap:"wrap",gap:2}}>
                {articleData.map((article)=> (
                    <ArticleCard title={article.title} link={article.link} key={article.link} />))}
            </Box>
        </div>
    )   
}
