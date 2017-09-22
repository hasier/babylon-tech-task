create or replace function random_string(length integer) returns text as
$$
declare
  chars text[] := '{0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}';
  result text := '';
  i integer := 0;
begin
  if length < 0 then
    raise exception 'Given length cannot be less than 0';
  end if;
  for i in 1..length loop
    result := result || chars[ceil(35 * random())];
  end loop;
  return result;
end;
$$ language plpgsql;

create or replace function gen_random_url()
returns trigger as $gen_random_url$
DECLARE
  random_url short_url.shortened_url%TYPE;
  len integer := 6;
  i integer := 0;
BEGIN
  random_url := random_string(len);
  while exists (select 1 from short_url su where su.shortened_url = random_url) loop
    random_url := random_string(len);
    i := i + 1;
    if i > 5 then
      len := len + 1;
    END IF;
  END LOOP;
  NEW.shortened_url := random_url;
  RETURN NEW;
END;
$gen_random_url$ language plpgsql;

DROP TRIGGER IF EXISTS gen_random_url ON short_url;

CREATE TRIGGER gen_random_url
before insert on short_url
FOR EACH ROW
WHEN (NEW.shortened_url is null)
EXECUTE PROCEDURE gen_random_url();
