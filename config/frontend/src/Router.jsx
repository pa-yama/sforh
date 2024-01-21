import React from "react";
import { createBrowserRouter } from "react-router-dom";
import { Detail } from "./component/detail";
import { CreatePost } from "./component/createPost";

import App from './App';
export const router = createBrowserRouter([
    //{ path: "index", element: <App /> },//reactビルド時はこれ(urls.pyの設定と合わせないと動かない？)
    { path: "", element: <App /> },//react開発時はこれ
    { path: "detail/:id", element: <Detail /> },
    { path: "createPost/", element: <CreatePost/> },//ヘッダーから

    { path: "createPost/edit/:id", element: <CreatePost/> },//詳細画面から
    { path: "createPost/tmpEdit/:id", element: <CreatePost/> },//一時保存中リストから



    //{ path: "detail/:id/goodPost", element: <Detail /> },
    //{ path: "detail/:id/unlikePost", element: <Detail /> },

  ]);