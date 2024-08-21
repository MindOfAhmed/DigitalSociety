import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import { Post } from "./Post";

export const PostPage = () => {
  // retrive the post id from the URL
  const { postId } = useParams();
  // define state variable to store the post data
  const [post, setPost] = useState(null);

  // on mount, fetch the post data
  useEffect(() => {
    try {
      // make an API call to fetch the post data
      (async () => {
        const response = await axios.get(
          `http://127.0.0.1:8080/api/get_post/${postId}/`
        );
        if (!response || !response.data) {
          throw new Error("Invalid server response");
        }
        // store the post data in state
        setPost(response.data);
      })();
    } catch (error) {
      console.error("Failed to fetch post", error);
    }
  }, [postId]);

  if (!post) {
    return <div>Loading...</div>;
  }
  console.log("post: ", post);

  return <Post post={post} />;
};
