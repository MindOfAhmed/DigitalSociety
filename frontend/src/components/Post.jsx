import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faThumbsUp, faComment } from "@fortawesome/free-solid-svg-icons";
import { useState } from "react";
import axios from "axios";

export const Post = ({ post, commentsCount }) => {
  // define state variable to control comment form's visibility
  const [showCommentForm, setShowCommentForm] = useState(false);
  // define state variable to store the comment data
  const [comment, setComment] = useState("");
  // define state cariable to store the likes count
  const [likesCount, setLikesCount] = useState(post.likes_count);

  // define the form submission handler
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // make an API call to submit the comment
      const response = await axios.post(
        `http://127.0.0.1:8080/api/create_comment/${post.id}/`,
        {
          content: comment,
        }
      );
      if (!response || !response.data) {
        throw new Error("Invalid server response");
      }
      // reset the comment form
      setComment("");
      // hide the comment form
      setShowCommentForm(false);
    } catch (error) {}
  };
  // define a handler for when the thumbs up icon is clicked
  const handleLikeCount = async () => {
    try {
      // make an API call to update the like count
      const response = await axios.post(
        `http://127.0.0.1:8080/api/update_likes/${post.id}/`
      );
      if (!response || !response.data) {
        throw new Error("Invalid server response");
      }
      console.log(response.data);
      // update the likes count in state
      setLikesCount(response.data.likes_count); // copilot ^_^
    } catch (error) {
      console.error("Failed to update like count", error);
    }
  };

  return (
    <div className="row m-3">
      <div className="d-flex justify-content-between align-items-center">
        <div className="d-flex gap-2 align-items-center">
          <img
            src={post.picture}
            alt="profile"
            className="post_profile_picture"
          />
          <p className="m-0">{post.author}</p>
        </div>
        <h1 className="text-center flex-grow-1">{post.title}</h1>
      </div>
      <p className="mt-2">{post.content}</p>
      <div className="d-flex gap-3 align-items-center">
        <span>
          <FontAwesomeIcon
            icon={faThumbsUp}
            onClick={handleLikeCount}
            className="me-2"
          />
          {likesCount}
        </span>
        <span>
          <FontAwesomeIcon
            icon={faComment}
            onClick={() => setShowCommentForm((s) => !s)}
            className="me-2"
          />
          {commentsCount}
        </span>
      </div>
      {showCommentForm && (
        <form className="mt-3" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="comment">Comment</label>
            <textarea
              className="form-control"
              id="comment"
              rows="3"
              placeholder="Write your comment here"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
            ></textarea>
          </div>
          <button type="submit" className="button mt-2">
            Submit
          </button>
        </form>
      )}
    </div>
  );
};
//style={{ backgroundColor: "pink" }}
