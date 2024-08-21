export const Comment = ({ comment }) => {
  return (
    <div className="row m-3 d-flex gap-2 align-items-center justify-content-center">
      <div className="col-md-6 card shadow p-2">
        <div className="d-flex justify-content-between align-items-center">
          <div className="d-flex gap-2 align-items-center">
            <img
              src={comment.picture}
              alt="profile"
              className="comment_profile_picture"
            />
            <p className="m-0">{comment.author}</p>
          </div>
          <p className="m-0">{comment.timestamp}</p>
        </div>
        <p className="mt-2">{comment.content}</p>
      </div>
    </div>
  );
};
