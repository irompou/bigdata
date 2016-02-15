
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
    owner_display_name, last_editor_user_id, last_editor_display_name,
    last_edit_date, last_activity_date, title, tags, answer_count,
    comment_count, favorite_count, closed_date, community_owned_date)
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

-- Enable the identity insert safety now that we're finished 
SET IDENTITY_INSERT posts OFF;
