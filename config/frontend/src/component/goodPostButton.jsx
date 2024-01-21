import axios from 'axios';
import React, {useState, useEffect} from 'react';
import { useNavigate } from 'react-router-dom';

const GoodPostButton = (props) => {
    
    const navigate = useNavigate();
    //propsで受け取れていることの確認
    console.log(props.post_id)

    let a = 1

    //axios初回のみ起動
    useEffect(() => {     
        axios.post('http://127.0.0.1:8000/detail/'  + props.post_id + '/goodPost/')
    }, [a]);


    const goodPost = async() =>{
            
        const post_id = props.post_id
        
        //navigate('/page1/' + props.post_id);
        //navigate('/detail/' + props.post_id + '/goodPost');

        //axios.defaults.baseURL = 'http://localhost:3000';
        //axios.defaults.xsrfCookieName = 'csrftoken'
        //axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

       
        a = a + 1

        


    };

    return(
        <>
        <button onClick={goodPost}>いいね</button>
        </>

    );
}

export default GoodPostButton