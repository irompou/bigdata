
DECLARE @xmlData XML;

-- Tags
SET @xmlData = (
  SELECT * FROM OPENROWSET (
    BULK 'C:\install\so_data\Tags.xml', SINGLE_CLOB
  ) AS xmlData
);

INSERT INTO tags(id, name, count)
SELECT 
  ref.value('@Id', 'int'),
  ref.value('@TagName', 'NVARCHAR (128)'),
  ref.value('@Count', 'int')
FROM @xmlData.nodes('//tags/row') xmlData(ref);




-- Users
SET @xmlData = (
  SELECT * FROM OPENROWSET (
    BULK 'C:\install\so_data\Users.xml', SINGLE_BLOB
  ) AS xmlData
);

INSERT INTO users(id, reputation, display_name, age, 
                  creation_date, last_access_date, website_url, 
                  [location], about_me, views, upvotes, downvotes)
SELECT 
    ref.value('@Id', 'int'), 
    ref.value('@Reputation', 'int'), 
    ref.value('@DisplayName', 'nvarchar(255)'), 
    ref.value('@Age', 'int'),
    ref.value('@CreationDate', 'datetime'),
    ref.value('@LastAccessDate', 'datetime'), 
    ref.value('@WebsiteUrl', 'nvarchar(2083)'), 
    ref.value('@Location', 'nvarchar(255)'), 
    ref.value('@AboutMe', 'nvarchar(max)'), 
    ref.value('@Views', 'int'), 
    ref.value('@UpVotes', 'int'),
    ref.value('@DownVotes', 'int')
FROM @xmlData.nodes('//users/row') xmlData(ref);




-- Post Types
INSERT INTO post_types(id, name)
VALUES
    (1, 'Question'),
    (2, 'Answer'),
    (3, 'Wiki'),
    (4, 'TagWikiExcerpt'),
    (5, 'TagWiki'),
    (6, 'ModeratorNomination'),
    (7, 'WikiPlaceholder'),
    (8, 'PrivilegeWiki');

-- Posts
SET @xmlData = (
  SELECT * FROM OPENROWSET (
    BULK 'C:\install\so_data\Posts.xml', SINGLE_BLOB
  ) AS xmlData
);

INSERT INTO posts(id, post_type_id, accepted_answer_id, parent_id,
                  creation_date, score, view_count, body, owner_user_id,
                  owner_display_name, last_editor_user_id, 
                  last_editor_display_name, last_edit_date, last_activity_date, 
                  title, tags, answer_count, comment_count, favorite_count, 
                  closed_date, community_owned_date)
SELECT 
    ref.value('@Id', 'int'),
    ref.value('@PostTypeId', 'int'),
    ref.value('@AcceptedAnswerId', 'int'),
    ref.value('@ParentId', 'int'),
    ref.value('@CreationDate', 'datetime'),
    ref.value('@Score', 'int'),
    ref.value('@ViewCount', 'int'),
    ref.value('@Body', 'nvarchar(max)'),
    ref.value('@OwnerUserId', 'int'),
    ref.value('@OwnerDisplayName', 'nvarchar(255)'),
    ref.value('@LastEditorUserId', 'int'),
    ref.value('@LastEditorDisplayName', 'nvarchar(255)'),
    ref.value('@LastEditDate', 'datetime'),
    ref.value('@LastActivityDate', 'datetime'),
    ref.value('@Title', 'nvarchar(511)'),
    ref.value('@Tags', 'nvarchar(max)'),
    ref.value('@AnswerCount', 'int'),
    ref.value('@CommentCount', 'int'),
    ref.value('@FavoriteCount', 'int'),
    ref.value('@ClosedDate', 'datetime'),
    ref.value('@CommunityOwnedDate', 'datetime')    
FROM @xmlData.nodes('//posts/row') xmlData(ref);




-- Comments
SET @xmlData = (
  SELECT * FROM OPENROWSET (
    BULK 'C:\install\so_data\Comments.xml', SINGLE_BLOB
  ) AS xmlData
);

INSERT INTO comments(id, post_id, score, text creation_date, 
                     user_display_name, user_id)
SELECT 
    ref.value('@Id', 'int'),
    ref.value('@PostId', 'int'),
    ref.value('@Score', 'int'),
    ref.value('@Text', 'nvarchar(max)'),
    ref.value('@CreationDate', 'datetime'),
    ref.value('@UserDisplayName', 'nvarchar(255)'),
    ref.value('@UserId', 'int')    
FROM @xmlData.nodes('//comments/row') xmlData(ref);




-- Vote Types
INSERT INTO vote_types(id, name)
VALUES
    (1, 'AcceptedByOriginator'),
    (2, 'UpMod'),
    (3, 'DownMod'),
    (4, 'Offensive'),
    (5, 'Favorite'),
    (6, 'Close'),
    (7, 'Reopen'),
    (8, 'BountyStart'),
    (9, 'BountyClose'),
    (10, 'Deletion'),
    (11, 'Undeletion'),
    (12, 'Spam'),
    (15, 'ModeratorReview'),
    (16, 'ApproveEditSuggestion');

-- Votes


-- Create a temporary table without constraints to just insert the data
CREATE TABLE #temp_votes (
    id INT PRIMARY KEY,
    post_id INT, -- foreign key
    vote_type_id INT NOT NULL, -- foreign key
    user_id INT, -- foreign key
    creation_date DATETIME NOT NULL,
    bounty_amount INT
);

SET @xmlData = (
  SELECT * FROM OPENROWSET (
    BULK 'C:\install\so_data\Votes.xml', SINGLE_BLOB
  ) AS xmlData
);

INSERT INTO #temp_votes(id, post_id, vote_type_id, user_id,
                        creation_date, bounty_amount)
SELECT 
    ref.value('@Id', 'int'),
    ref.value('@PostId', 'int'),
    ref.value('@VoteTypeId', 'int'),
    ref.value('@UserId', 'int'),
    ref.value('@CreationDate', 'DATETIME'),
    ref.value('@BountyAmount', 'int')
FROM @xmlData.nodes('//votes/row') xmlData(ref);


-- Some of the votes reference non-existent/deleted posts,
-- so we have to remove them before inserting to the real table
DELETE #temp_votes
WHERE 
    post_id NOT IN (SELECT id from posts);


-- Now we can safely insert the curated data to the real table
INSERT INTO votes(id, post_id, vote_type_id, user_id,
                  creation_date, bounty_amount)
SELECT 
    id, post_id, vote_type_id, user_id,
    creation_date, bounty_amount 
FROM #temp_votes;

DROP TABLE #temp_votes;

