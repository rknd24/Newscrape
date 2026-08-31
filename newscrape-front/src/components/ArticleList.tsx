import ArticleCard from "./ArticleCard"
import { useState } from "react"
import { useEffect } from "react"

export default function ArticleList(){
    const [articleData,setArticleData] = useState<any>([])
    useEffect(() => {
        fetch("/news/1").then(res => res.json()).then(data => {
            setArticleData(data.articles)
        })
    },[])
    return(
        articleData.map((article,index)=>
        <ArticleCard title={article.title} key={index} />
    )
)
}
