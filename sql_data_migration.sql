select *
from timezones;
select id, IF(statu, 'true', 'false') as statu
from `system`;
select *
from quick_answers;
select *
from webview;
select id,
       name,
       last_name,
       email,
       email_verified_at,
       password,
       email_token,
       timezone,
       pp,
       type,
       os,
       status,
       auto_zone,
       remember_token,
       created_at,
       updated_at,
       pause_start,
       pause_end,
       payment_day,
       parent,
       IF(archive, 'true', 'false') as archive,
       device,
       elasticid
from users;

select id,
       from_user,
       to_user,
       type,
       content,
       path,
       IF(is_seen, 'true', 'false') as is_seen,
       created_at,
       updated_at,
       deleted_at,
       log
from messages; -- copy to file

select *
from diets;
select *
from breakfast_logs;
select *
from dinner_logs;
select *
from lunch_logs;
select *
from walking_logs;
select *
from weight_logs;

select *
from sport;
select *
from water;
select id,
       user_id,
       age,
       weight,
       height,
       notes,
       type,
       gender,
       IF(can_walk, 'true', 'false') as can_walk,
       IF(vip, 'true', 'false') as vip,
       target,
       created_at,
       updated_at,
       begining
from user_infos;
select * from delete_approves; # 17 den yukarısı insert oluyor

select * from diet_repeats;
select * from diet_images;
