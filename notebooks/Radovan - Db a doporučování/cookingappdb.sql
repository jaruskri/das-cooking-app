--
-- PostgreSQL database dump
--

-- Dumped from database version 12.0
-- Dumped by pg_dump version 12.0

-- Started on 2019-12-10 18:39:54

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
-- TOC entry 220 (class 1255 OID 17097)
-- Name: nantonull(); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.nantonull()
    LANGUAGE plpgsql
    AS $$BEGIN
UPDATE recept SET calories=NULL WHERE calories='NaN';
UPDATE recept SET protein=NULL WHERE protein='NaN';
UPDATE recept SET sodium=NULL WHERE sodium='NaN';
UPDATE recept SET fat=NULL WHERE fat='NaN';
END;$$;


ALTER PROCEDURE public.nantonull() OWNER TO postgres;

--
-- TOC entry 221 (class 1255 OID 25109)
-- Name: truncate_all(); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.truncate_all()
    LANGUAGE plpgsql
    AS $$BEGIN
TRUNCATE zvolene_kategorie CASCADE;
TRUNCATE zvolene_ingredience CASCADE;
TRUNCATE ingredience CASCADE;
TRUNCATE postup CASCADE;
TRUNCATE ingredience_v_receptu CASCADE;
TRUNCATE ingredience_pref CASCADE;
TRUNCATE prislusnost_kategorii CASCADE;
TRUNCATE kategorie CASCADE;
TRUNCATE recept CASCADE;
ALTER SEQUENCE ingredience_pref_iid_seq RESTART WITH 1;
ALTER SEQUENCE kategorie_kid_seq RESTART WITH 1;
ALTER SEQUENCE recept_rid_seq RESTART WITH 1;
END;$$;


ALTER PROCEDURE public.truncate_all() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 208 (class 1259 OID 16899)
-- Name: ingredience; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ingredience (
    text text NOT NULL,
    idr bigint NOT NULL
);


ALTER TABLE public.ingredience OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 16914)
-- Name: ingredience_pref; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ingredience_pref (
    iid integer NOT NULL,
    nazev text NOT NULL
);


ALTER TABLE public.ingredience_pref OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16912)
-- Name: ingredience_pref_iid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ingredience_pref_iid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ingredience_pref_iid_seq OWNER TO postgres;

--
-- TOC entry 2929 (class 0 OID 0)
-- Dependencies: 209
-- Name: ingredience_pref_iid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ingredience_pref_iid_seq OWNED BY public.ingredience_pref.iid;


--
-- TOC entry 211 (class 1259 OID 16925)
-- Name: ingredience_v_receptu; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ingredience_v_receptu (
    idr bigint NOT NULL,
    idi bigint NOT NULL
);


ALTER TABLE public.ingredience_v_receptu OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 17086)
-- Name: ingredienci_v_receptu; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.ingredienci_v_receptu AS
 SELECT ingredience_v_receptu.idr,
    count(ingredience_v_receptu.idr) AS pocet_ingredienci
   FROM public.ingredience_v_receptu
  GROUP BY ingredience_v_receptu.idr;


ALTER TABLE public.ingredienci_v_receptu OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 16847)
-- Name: kategorie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kategorie (
    kid integer NOT NULL,
    nazev text NOT NULL
);


ALTER TABLE public.kategorie OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 16845)
-- Name: kategorie_kid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kategorie_kid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kategorie_kid_seq OWNER TO postgres;

--
-- TOC entry 2934 (class 0 OID 0)
-- Dependencies: 202
-- Name: kategorie_kid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kategorie_kid_seq OWNED BY public.kategorie.kid;


--
-- TOC entry 206 (class 1259 OID 16871)
-- Name: prislusnost_kategorii; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prislusnost_kategorii (
    idr bigint NOT NULL,
    idk bigint NOT NULL
);


ALTER TABLE public.prislusnost_kategorii OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 16862)
-- Name: recept; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.recept (
    rid integer NOT NULL,
    calories double precision,
    description text,
    protein double precision,
    rating double precision,
    title text NOT NULL,
    sodium double precision,
    date timestamp without time zone,
    fat double precision
);


ALTER TABLE public.recept OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 17048)
-- Name: zvolene_kategorie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.zvolene_kategorie (
    idk bigint NOT NULL
);


ALTER TABLE public.zvolene_kategorie OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 17058)
-- Name: recept_vyhovujici_kategorii; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.recept_vyhovujici_kategorii AS
 SELECT shoda.idr
   FROM ( SELECT recept.rid AS idr,
            count(recept.rid) AS count
           FROM (((public.kategorie
             JOIN public.prislusnost_kategorii ON ((kategorie.kid = prislusnost_kategorii.idk)))
             RIGHT JOIN public.zvolene_kategorie ON ((kategorie.kid = zvolene_kategorie.idk)))
             JOIN public.recept ON ((prislusnost_kategorii.idr = recept.rid)))
          GROUP BY recept.rid) shoda
  WHERE (shoda.count = ( SELECT count(*) AS count
           FROM public.zvolene_kategorie));


ALTER TABLE public.recept_vyhovujici_kategorii OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 17063)
-- Name: zvolene_ingredience; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.zvolene_ingredience (
    idi bigint NOT NULL
);


ALTER TABLE public.zvolene_ingredience OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 17073)
-- Name: shoda_ingredienci; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.shoda_ingredienci WITH (security_barrier='false') AS
 SELECT ings.idr,
    ings.shoda,
    ( SELECT count(*) AS count
           FROM public.zvolene_ingredience) AS zvoleno_ingredienci
   FROM ( SELECT ingredience_v_receptu.idr,
            count(ingredience_v_receptu.idr) AS shoda
           FROM (public.ingredience_v_receptu
             JOIN public.zvolene_ingredience ON ((ingredience_v_receptu.idi = zvolene_ingredience.idi)))
          GROUP BY ingredience_v_receptu.idr) ings;


ALTER TABLE public.shoda_ingredienci OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 17090)
-- Name: navrzene_recepty; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.navrzene_recepty WITH (security_barrier='false') AS
 SELECT recept.rid,
    shoda_ingredienci.shoda,
    shoda_ingredienci.zvoleno_ingredienci,
    ingredienci_v_receptu.pocet_ingredienci,
    recept.calories,
    recept.protein,
    recept.rating,
    recept.sodium,
    recept.fat,
    recept.title,
    recept.description,
    recept.date
   FROM (((public.recept
     JOIN public.ingredienci_v_receptu ON ((recept.rid = ingredienci_v_receptu.idr)))
     JOIN public.recept_vyhovujici_kategorii ON ((recept.rid = recept_vyhovujici_kategorii.idr)))
     JOIN public.shoda_ingredienci ON ((recept.rid = shoda_ingredienci.idr)));


ALTER TABLE public.navrzene_recepty OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 16886)
-- Name: postup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.postup (
    idr bigint NOT NULL,
    text text NOT NULL,
    poradi bigint NOT NULL
);


ALTER TABLE public.postup OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 16860)
-- Name: recept_rid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.recept_rid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recept_rid_seq OWNER TO postgres;

--
-- TOC entry 2944 (class 0 OID 0)
-- Dependencies: 204
-- Name: recept_rid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.recept_rid_seq OWNED BY public.recept.rid;


--
-- TOC entry 218 (class 1259 OID 17101)
-- Name: zvolene_ingredience2; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.zvolene_ingredience2 AS
 SELECT zvolene_ingredience.idi,
    ingredience_pref.iid,
    ingredience_pref.nazev
   FROM (public.zvolene_ingredience
     JOIN public.ingredience_pref ON ((zvolene_ingredience.idi = ingredience_pref.iid)));


ALTER TABLE public.zvolene_ingredience2 OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 17105)
-- Name: zvolene_kategorie2; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.zvolene_kategorie2 AS
 SELECT zvolene_kategorie.idk,
    kategorie.kid,
    kategorie.nazev
   FROM (public.zvolene_kategorie
     JOIN public.kategorie ON ((kategorie.kid = zvolene_kategorie.idk)));


ALTER TABLE public.zvolene_kategorie2 OWNER TO postgres;

--
-- TOC entry 2756 (class 2604 OID 16917)
-- Name: ingredience_pref iid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredience_pref ALTER COLUMN iid SET DEFAULT nextval('public.ingredience_pref_iid_seq'::regclass);


--
-- TOC entry 2754 (class 2604 OID 16850)
-- Name: kategorie kid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kategorie ALTER COLUMN kid SET DEFAULT nextval('public.kategorie_kid_seq'::regclass);


--
-- TOC entry 2755 (class 2604 OID 16865)
-- Name: recept rid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recept ALTER COLUMN rid SET DEFAULT nextval('public.recept_rid_seq'::regclass);


--
-- TOC entry 2768 (class 2606 OID 16906)
-- Name: ingredience ingredience_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredience
    ADD CONSTRAINT ingredience_pkey PRIMARY KEY (text, idr);


--
-- TOC entry 2772 (class 2606 OID 16924)
-- Name: ingredience_pref ingredience_pref_nazev_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredience_pref
    ADD CONSTRAINT ingredience_pref_nazev_key UNIQUE (nazev);


--
-- TOC entry 2774 (class 2606 OID 16922)
-- Name: ingredience_pref ingredience_pref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredience_pref
    ADD CONSTRAINT ingredience_pref_pkey PRIMARY KEY (iid);


--
-- TOC entry 2770 (class 2606 OID 25144)
-- Name: ingredience ingredience_text_idr_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredience
    ADD CONSTRAINT ingredience_text_idr_key UNIQUE (text, idr);


--
-- TOC entry 2776 (class 2606 OID 16929)
-- Name: ingredience_v_receptu ingredience_v_receptu_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredience_v_receptu
    ADD CONSTRAINT ingredience_v_receptu_pkey PRIMARY KEY (idr, idi);


--
-- TOC entry 2758 (class 2606 OID 16857)
-- Name: kategorie kategorie_nazev_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kategorie
    ADD CONSTRAINT kategorie_nazev_key UNIQUE (nazev);


--
-- TOC entry 2760 (class 2606 OID 16855)
-- Name: kategorie kategorie_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kategorie
    ADD CONSTRAINT kategorie_pkey PRIMARY KEY (kid);


--
-- TOC entry 2766 (class 2606 OID 16893)
-- Name: postup postup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postup
    ADD CONSTRAINT postup_pkey PRIMARY KEY (idr, poradi);


--
-- TOC entry 2764 (class 2606 OID 16875)
-- Name: prislusnost_kategorii prislusnost_kategorii_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prislusnost_kategorii
    ADD CONSTRAINT prislusnost_kategorii_pkey PRIMARY KEY (idr, idk);


--
-- TOC entry 2762 (class 2606 OID 16870)
-- Name: recept recept_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recept
    ADD CONSTRAINT recept_pkey PRIMARY KEY (rid);


--
-- TOC entry 2780 (class 2606 OID 17067)
-- Name: zvolene_ingredience zvolene_ingredience_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.zvolene_ingredience
    ADD CONSTRAINT zvolene_ingredience_pkey PRIMARY KEY (idi);


--
-- TOC entry 2778 (class 2606 OID 17052)
-- Name: zvolene_kategorie zvolene_kategorie_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.zvolene_kategorie
    ADD CONSTRAINT zvolene_kategorie_pkey PRIMARY KEY (idk);


--
-- TOC entry 2784 (class 2606 OID 16907)
-- Name: ingredience ingredience_idr_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredience
    ADD CONSTRAINT ingredience_idr_fkey FOREIGN KEY (idr) REFERENCES public.recept(rid) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 2786 (class 2606 OID 16935)
-- Name: ingredience_v_receptu ingredience_v_receptu_idi_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredience_v_receptu
    ADD CONSTRAINT ingredience_v_receptu_idi_fkey FOREIGN KEY (idi) REFERENCES public.ingredience_pref(iid) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 2785 (class 2606 OID 16930)
-- Name: ingredience_v_receptu ingredience_v_receptu_idr_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredience_v_receptu
    ADD CONSTRAINT ingredience_v_receptu_idr_fkey FOREIGN KEY (idr) REFERENCES public.recept(rid) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 2783 (class 2606 OID 16894)
-- Name: postup postup_idr_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postup
    ADD CONSTRAINT postup_idr_fkey FOREIGN KEY (idr) REFERENCES public.recept(rid) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 2782 (class 2606 OID 16881)
-- Name: prislusnost_kategorii prislusnost_kategorii_idk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prislusnost_kategorii
    ADD CONSTRAINT prislusnost_kategorii_idk_fkey FOREIGN KEY (idk) REFERENCES public.kategorie(kid) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 2781 (class 2606 OID 16876)
-- Name: prislusnost_kategorii prislusnost_kategorii_idr_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prislusnost_kategorii
    ADD CONSTRAINT prislusnost_kategorii_idr_fkey FOREIGN KEY (idr) REFERENCES public.recept(rid) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 2788 (class 2606 OID 17068)
-- Name: zvolene_ingredience zvolene_ingredience_idi_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.zvolene_ingredience
    ADD CONSTRAINT zvolene_ingredience_idi_fkey FOREIGN KEY (idi) REFERENCES public.ingredience_pref(iid) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 2787 (class 2606 OID 17053)
-- Name: zvolene_kategorie zvolene_kategorie_idk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.zvolene_kategorie
    ADD CONSTRAINT zvolene_kategorie_idk_fkey FOREIGN KEY (idk) REFERENCES public.kategorie(kid);


--
-- TOC entry 2926 (class 0 OID 0)
-- Dependencies: 220
-- Name: PROCEDURE nantonull(); Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON PROCEDURE public.nantonull() TO cook;


--
-- TOC entry 2927 (class 0 OID 0)
-- Dependencies: 208
-- Name: TABLE ingredience; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.ingredience TO cook;


--
-- TOC entry 2928 (class 0 OID 0)
-- Dependencies: 210
-- Name: TABLE ingredience_pref; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.ingredience_pref TO cook;


--
-- TOC entry 2930 (class 0 OID 0)
-- Dependencies: 209
-- Name: SEQUENCE ingredience_pref_iid_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.ingredience_pref_iid_seq TO cook;


--
-- TOC entry 2931 (class 0 OID 0)
-- Dependencies: 211
-- Name: TABLE ingredience_v_receptu; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.ingredience_v_receptu TO cook;


--
-- TOC entry 2932 (class 0 OID 0)
-- Dependencies: 216
-- Name: TABLE ingredienci_v_receptu; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.ingredienci_v_receptu TO cook;


--
-- TOC entry 2933 (class 0 OID 0)
-- Dependencies: 203
-- Name: TABLE kategorie; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.kategorie TO cook;


--
-- TOC entry 2935 (class 0 OID 0)
-- Dependencies: 202
-- Name: SEQUENCE kategorie_kid_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.kategorie_kid_seq TO cook;


--
-- TOC entry 2936 (class 0 OID 0)
-- Dependencies: 206
-- Name: TABLE prislusnost_kategorii; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.prislusnost_kategorii TO cook;


--
-- TOC entry 2937 (class 0 OID 0)
-- Dependencies: 205
-- Name: TABLE recept; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.recept TO cook;


--
-- TOC entry 2938 (class 0 OID 0)
-- Dependencies: 212
-- Name: TABLE zvolene_kategorie; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.zvolene_kategorie TO cook;


--
-- TOC entry 2939 (class 0 OID 0)
-- Dependencies: 213
-- Name: TABLE recept_vyhovujici_kategorii; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.recept_vyhovujici_kategorii TO cook;


--
-- TOC entry 2940 (class 0 OID 0)
-- Dependencies: 214
-- Name: TABLE zvolene_ingredience; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.zvolene_ingredience TO cook;


--
-- TOC entry 2941 (class 0 OID 0)
-- Dependencies: 215
-- Name: TABLE shoda_ingredienci; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.shoda_ingredienci TO cook;


--
-- TOC entry 2942 (class 0 OID 0)
-- Dependencies: 217
-- Name: TABLE navrzene_recepty; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.navrzene_recepty TO cook;


--
-- TOC entry 2943 (class 0 OID 0)
-- Dependencies: 207
-- Name: TABLE postup; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.postup TO cook;


--
-- TOC entry 2945 (class 0 OID 0)
-- Dependencies: 204
-- Name: SEQUENCE recept_rid_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.recept_rid_seq TO cook;


-- Completed on 2019-12-10 18:39:54

--
-- PostgreSQL database dump complete
--

