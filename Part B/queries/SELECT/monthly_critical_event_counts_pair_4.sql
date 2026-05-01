select distinct
  EXTRACT(
    year
    from
      p.start_time
  ) as yr,
  EXTRACT(
    month
    from
      p.start_time
  ) as mo,
  (
    select
      COUNT(*)
    from
      SYSTEM_EVENTS s2
      join PROCESSES p2 on s2.pid = p2.pid
    where
      EXTRACT(
        year
        from
          p2.start_time
      ) = EXTRACT(
        year
        from
          p.start_time
      )
      and EXTRACT(
        month
        from
          p2.start_time
      ) = EXTRACT(
        month
        from
          p.start_time
      )
      and s2.severity = 'Critical'
  ) as total_events
from
  SYSTEM_EVENTS s
  join PROCESSES p on s.pid = p.pid
where
  s.severity = 'Critical'
order by
  yr desc,
  mo desc;
