import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import { Post } from "./Post";
import { Comment } from "./Comment";

export const PostPage = () => {
  // retrive the post id from the URL
  const { postId } = useParams();
  // define state variable to store the post data
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  /* define state variable to store the logged in user's username. 
  this will be used to allow authors to delete their content */
  const [loggedUser, setLoggedUser] = useState("");

  // on mount, fetch the post data
  useEffect(() => {
    try {
      // make an API call to fetch the post data
      (async () => {
        const PostResponse = await axios.get(
          `http://127.0.0.1:8080/api/get_post/${postId}/`
        );
        if (!PostResponse || !PostResponse.data) {
          throw new Error("Invalid server response");
        }
        // store the post data in state
        setPost(PostResponse.data);
        const CommentsResponse = await axios.get(
          `http://127.0.0.1:8080/api/get_comments/${postId}/`
        );
        if (!CommentsResponse || !CommentsResponse.data) {
          throw new Error("Invalid server response");
        }
        // store the post data in state
        setComments(CommentsResponse.data);
        // fetch the current logged in user's username
        const userResponse = await axios.get(
          "http://127.0.0.1:8080/api/get_user/"
        );
        if (!userResponse || !userResponse.data) {
          throw new Error("Invalid server response");
        }
        // store the logged in user's username in state
        setLoggedUser(userResponse.data.username);
      })();
    } catch (error) {
      console.error("Failed to fetch post", error);
    }
  }, [postId]);

  if (!post) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <Post
        post={post}
        commentsCount={comments.length}
        loggedUser={loggedUser}
      />
      <hr />
      {/* comments */}
      {comments &&
        comments.length > 0 &&
        comments.map((comment, index) => (
          <Comment key={index} comment={comment} loggedUser={loggedUser} />
        ))}
    </>
  );
};
