import axios from 'axios';
import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';

const CreatePostEditButton = (props) => {
    
    const navigate = useNavigate();
    //propsで受け取れていることの確認
    console.log(props.post_id)

    const createPostPage = () =>{
            
        //const post_id = props.post_id
        
        //navigate('/page1/' + props.post_id);
        
        navigate('/createPost/edit/' + props.post_id);
    };

    return(
        <>
        <button onClick={createPostPage}>投稿作成</button>
        </>

    );
}

export default CreatePostEditButton