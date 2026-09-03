import ArticleCard from "./ArticleCard"
import { useState,useEffect } from "react"
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { type SelectChangeEvent } from '@mui/material/Select';
import {getNews,type Article} from "../api"
import Button from '@mui/material/Button';
import Search_Bar from "./SearchBar";

type Status = "idle" | "loading" | "success" | "error"

export default function ArticleList(){
    const [articleData,setArticleData] = useState<Article[]>([])
    const [category,setCategory] = useState("top-picks")
    const [query,setQuery] = useState("")
    const [state,setState] = useState<Status>("idle")
    const loadNews = () => {
        setState("loading")
        getNews(category,query).then(articles => {
            setState("success")
            setArticleData(articles)
        })
        .catch(() => setState("error"))
    }
        useEffect(() => {
            loadNews()
        }, [category,query])
    const handleChange = (event: SelectChangeEvent) => {
        setCategory(event.target.value as string);
    };
    const onSearch = (word:string) => {
        setQuery(word)
    }
    return(
        <div>
            <Search_Bar onSearch={onSearch}/>
            {state == "loading" && <p>NowLoading…</p>}
            {state == "error" && (
            <div>
                <p>読み込みに失敗しました。</p>
                <Button onClick={loadNews}>再読み込み</Button>
            </div>)}
            <FormControl sx={{ minWidth: 200, mb: 3 }}>
                <InputLabel id="demo-simple-select-label">category</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={category}
                    label="Category"
                    onChange={handleChange}
                >
                <MenuItem value="top-picks">総合</MenuItem>
                <MenuItem value="domestic">国内</MenuItem>
                <MenuItem value="world">国際</MenuItem>
                <MenuItem value="business">経済</MenuItem>
                <MenuItem value="entertainment">エンタメ</MenuItem>
                <MenuItem value="sports">スポーツ</MenuItem>
                <MenuItem value="it">IT</MenuItem>
                <MenuItem value="science">科学</MenuItem>
                <MenuItem value="local">地域</MenuItem>
                </Select>
            </FormControl>
            {state == "success" && (
                <Box sx={{display:"flex",flexWrap:"wrap",gap:2}}>
                    {articleData.map((article)=> (
                        <ArticleCard article={article} key={article.link} />))}
                </Box>
            )}
        </div>
    )   
}
