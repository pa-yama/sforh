import axios from 'axios';
import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';
import "../static/css/style.css";

const DetailButton = (props) => {
    
    const navigate = useNavigate();
    //propsで受け取れていることの確認
    //console.log(props.post_id)

    const detailPage = () =>{
            
        const post_id = props.post_id
        
        //navigate('/page1/' + props.post_id);
        navigate('/detail/' + props.post_id);
    };

    return(
        <>
        <button onClick={detailPage}>詳細ページへ</button>
        </>

    );
}

export default DetailButton