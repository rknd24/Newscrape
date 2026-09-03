import { useState } from "react";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

export default function Search_Bar({onSearch}:{onSearch:(word:string)=>void}){
    const [word,setWord] = useState("")
    const onSearchClick = () => {
      onSearch(word)
    }
    return(
      <Box
      component="form"
      onSubmit={(e) => {e.preventDefault(); onSearchClick()}}
      sx={{ '& > :not(style)': { m: 1, width: '25ch' } }}
      noValidate
      autoComplete="off"
    >
        <TextField 
        id="outlined-basic" 
        label="Search" 
        value={word} 
        onChange={(e) => setWord(e.target.value)} 
        variant="outlined" />
      </Box>
    )
}