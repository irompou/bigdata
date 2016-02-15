-- Tags
CREATE TABLE tags (
    id int PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    [count] int
);

CREATE UNIQUE NONCLUSTERED INDEX ix_tags_name ON tags(name);


-- Users
CREATE TABLE users (
    id int PRIMARY KEY,
    reputation int,
    display_name NVARCHAR(255) NOT NULL,
    age int,
    creation_date DATETIME,
    last_access_date DATETIME,
    website_url NVARCHAR(2083),
    [location] NVARCHAR(255),
    about_me NVARCHAR(MAX),
    views int,
    upvotes int,
    downvotes int
);


-- Post Types
CREATE TABLE post_types (
    id INT PRIMARY KEY,
    name NVARCHAR(255) NOT NULL
);

-- Posts
CREATE TABLE posts (
    id INT PRIMARY KEY,
    post_type_id INT NOT NULL, -- foreign key
    accepted_answer_id INT, -- foreign key
    parent_id int, -- foreign key
    creation_date DATETIME NOT NULL,
    score INT NOT NULL,
    view_count INT,
    body NVARCHAR(MAX) NOT NULL,
    owner_user_id INT, -- foreign key
    owner_display_name NVARCHAR(255),
    last_editor_user_id INT, -- foreign key
    last_editor_display_name NVARCHAR(255),
    last_edit_date DATETIME,
    last_activity_date DATETIME,
    title NVARCHAR(511),
    tags NVARCHAR(MAX),
    answer_count INT,
    comment_count INT,
    favorite_count INT,
    closed_date DATETIME,
    community_owned_date DATETIME,

    CONSTRAINT fk_posts_post_type FOREIGN KEY(post_type_id) REFERENCES post_types(id),
    CONSTRAINT fk_posts_accepted_answer FOREIGN KEY(accepted_answer_id) REFERENCES posts(id),
    CONSTRAINT fk_posts_parent FOREIGN KEY(parent_id) REFERENCES posts(id),
    CONSTRAINT fk_posts_owner_user FOREIGN KEY(owner_user_id) REFERENCES users(id),
    CONSTRAINT fk_posts_last_editor_user FOREIGN KEY(last_editor_user_id) REFERENCES users(id)
);


-- Comments
CREATE TABLE comments (
    id INT PRIMARY KEY,
    post_id INT NOT NULL, -- foreign key
    score INT,
    [text] NVARCHAR(MAX), 
    creation_date DATETIME NOT NULL,
    user_display_name NVARCHAR(255),
    user_id INT, -- foreign key

    CONSTRAINT fk_comments_post FOREIGN KEY(post_id) REFERENCES posts(id),
    CONSTRAINT fk_comments_user FOREIGN KEY(user_id) REFERENCES users(id)
);




-- Vote Types
CREATE TABLE vote_types (
    id INT PRIMARY KEY,
    name NVARCHAR(255) NOT NULL    
);


-- Votes
CREATE TABLE votes (
    id INT PRIMARY KEY,
    post_id INT, -- foreign key
    vote_type_id INT NOT NULL, -- foreign key
    user_id INT, -- foreign key
    creation_date DATETIME NOT NULL,
    bounty_amount INT,

    CONSTRAINT fk_votes_post FOREIGN KEY(post_id) REFERENCES posts(id),
    CONSTRAINT fk_votes_vote_type FOREIGN KEY(vote_type_id) REFERENCES vote_types(id),
    CONSTRAINT fk_votes_user FOREIGN KEY(user_id) REFERENCES users(id)
);
