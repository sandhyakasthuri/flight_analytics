CREATE DATABASE flight_analytics;

SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- airport table
ALTER TABLE airport ADD PRIMARY KEY (iata);
ALTER TABLE airport ADD UNIQUE (icao);

-- aircraft table
ALTER TABLE aircraft ADD PRIMARY KEY (registration);

-- flights table
ALTER TABLE flights ADD PRIMARY KEY (flight_id);

-- airport_delays table
ALTER TABLE airport_delays ADD PRIMARY KEY (airport_iata);

SELECT * FROM airport LIMIT 5;
SELECT * FROM flights LIMIT 5;
SELECT * FROM aircraft LIMIT 5;
SELECT * FROM airport_delays LIMIT 5;

select aircraft.model, count(flights.flight_number) as total_flights from flights
join aircraft on flights.aircraft_registration = aircraft.registration
group by aircraft.model

select aircraft.model, aircraft.registration from aircraft
join flights on flights.aircraft_registration = aircraft.registration
GROUP BY aircraft.registration, aircraft.model
having count(flights.flight_number) >5;

select airport."fullName", count(flights.flight_number) as outbound_flights from flights
join airport on airport.iata = flights.origin_iata
group by airport."fullName"
having count(flights.flight_number) >5;

select airport."fullName", airport.city,count(flights.destination_iata) as inbound_flights from airport
join flights on airport.iata = flights.destination_iata
group by airport."fullName", airport.city
order by inbound_flights desc
limit 3;

select flights.flight_number, origin_airport.country_code as origin_country,
dest_airport.country_code as dest_country,
case when origin_airport.country_code = dest_airport.country_code
then 'domestic'
else 'international'
end as flight_type
from flights
join airport AS origin_airport ON origin_airport.iata = flights.origin_iata
join airport as dest_airport on dest_airport.iata = flights.destination_iata;

select flight_number, aircraft_registration, scheduled_arrival as arrival_time, 
airport."fullName" as departure_airport from flights 
join airport on airport.iata = origin_iata
where flights.destination_iata ='DEL'
order by flights.scheduled_arrival desc
limit 5;

select airport.iata, airport."fullName"
from airport
left join flights on airport.iata = flights.destination_iata
where flights.destination_iata is null;

select distinct status from flights;

select 
    airline_code,
    count(case when status = 'Arrived' then 1 end) as arrived,
    count(case when status = 'Delayed' then 1 end) as delayed,
    count(case when status = 'Canceled' then 1 end) as cancelled,
    count(case when status = 'Departed' then 1 end) as departed,
    count(case when status = 'Unknown' then 1 end) as unknown
from flights
group by airline_code
order by airline_code;

select 
    flights.aircraft_registration,
    flights.scheduled_departure,
    origin_airport."fullName" as departure_airport,
    dest_airport."fullName" as arrival_airport
from flights
join airport as origin_airport on origin_airport.iata = flights.origin_iata
join airport as dest_airport on dest_airport.iata = flights.destination_iata
where flights.status = 'Canceled'
order by flights.scheduled_departure desc;

select 
    origin_airport.city as origin_city,
    dest_airport.city as dest_city,
    count(distinct aircraft.model) as different_models
from flights
join airport as origin_airport on origin_airport.iata = flights.origin_iata
join airport as dest_airport on dest_airport.iata = flights.destination_iata
join aircraft on aircraft.registration = flights.aircraft_registration
group by origin_airport.city, dest_airport.city
having count(distinct aircraft.model) > 2
order by different_models desc;

select 
    destination_iata,
    count(flight_id) as total_flights,
    count(case when status = 'Delayed' then 1 end) as delayed_flights,
    round(count(case when status = 'Delayed' then 1 end) * 100.0 / count(flight_id), 2) as delay_percentage
from flights
group by destination_iata
order by delay_percentage desc;