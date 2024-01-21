import axios from 'axios';
import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';

const UnlikePostButton = (props) => {
    
    const navigate = useNavigate();
    //propsで受け取れていることの確認
    console.log(props.post_id)

    const unlikePost = () =>{
            
        const post_id = props.post_id
        
        //navigate('/page1/' + props.post_id);
        axios.defaults.xsrfCookieName = 'csrftoken'
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
        
        navigate('/detail/' + props.post_id + '/unlikePost/');  
    };

    return(
        <>
        <button onClick={unlikePost}>いいね解除</button>
        </>

    );
}

export default UnlikePostButton