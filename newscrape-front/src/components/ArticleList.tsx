import ArticleCard from "./ArticleCard"
import { useState } from "react"
import { useEffect } from "react"

interface Article {
    title: string;
    link: string;
}

export default function ArticleList(){
    const [articleData,setArticleData] = useState<Article[]>([])
    useEffect(() => {
        fetch("/news/1").then(res => res.json()).then(data => {
            setArticleData(data.articles);
        })
    },[])
    return(
        articleData.map((article,index)=>
        <ArticleCard title={article.title} link={article.link} key={index} />
    )
)
}
