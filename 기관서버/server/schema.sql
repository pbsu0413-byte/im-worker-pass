-- Supabase SQL Editor에서 그대로 실행하세요.
-- 이 테이블이 곧 "발급기관이 원본 데이터를 들고 있는 더미 DB" 역할입니다.
-- (실제 서비스에서는 이 데이터가 근로자 스마트폰에 암호화 보관되지만,
--  웹 프로토타입에서는 시연 편의를 위해 서버 DB에 둡니다.)

create table if not exists credentials (
  credential_id uuid primary key default gen_random_uuid(),
  worker_name text not null,
  nationality text not null,
  account_bank text not null,
  account_number text not null,
  status text not null default 'valid' check (status in ('valid', 'revoked')),
  created_at timestamptz not null default now()
);

-- (선택) 시연용 초기 데이터
insert into credentials (worker_name, nationality, account_bank, account_number, status)
values
  ('NGUYEN VAN A', '베트남', 'iM뱅크', '512-123456-01', 'valid'),
  ('BAT-ERDENE', '몽골', 'iM뱅크', '512-987654-02', 'valid');
