--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8 (Ubuntu 16.8-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.8 (Ubuntu 16.8-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: todo_user
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO todo_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: dones; Type: TABLE; Schema: public; Owner: todo_user
--

CREATE TABLE public.dones (
    id integer NOT NULL
);


ALTER TABLE public.dones OWNER TO todo_user;

--
-- Name: tasks; Type: TABLE; Schema: public; Owner: todo_user
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    title character varying(1024)
);


ALTER TABLE public.tasks OWNER TO todo_user;

--
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: todo_user
--

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tasks_id_seq OWNER TO todo_user;

--
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todo_user
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: todo_user
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- Data for Name: dones; Type: TABLE DATA; Schema: public; Owner: todo_user
--

COPY public.dones (id) FROM stdin;
\.


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: todo_user
--

COPY public.tasks (id, title) FROM stdin;
\.


--
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: todo_user
--

SELECT pg_catalog.setval('public.tasks_id_seq', 1, false);


--
-- Name: dones dones_pkey; Type: CONSTRAINT; Schema: public; Owner: todo_user
--

ALTER TABLE ONLY public.dones
    ADD CONSTRAINT dones_pkey PRIMARY KEY (id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: todo_user
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: dones dones_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todo_user
--

ALTER TABLE ONLY public.dones
    ADD CONSTRAINT dones_id_fkey FOREIGN KEY (id) REFERENCES public.tasks(id);


--
-- PostgreSQL database dump complete
--

