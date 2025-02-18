PGDMP              	        {            lab_2    15.4    16.0 $    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16398    lab_2    DATABASE     y   CREATE DATABASE lab_2 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE lab_2;
                postgres    false            �            1255    16494    check_new_contract()    FUNCTION     '  CREATE FUNCTION public.check_new_contract() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN	
    -- Проверка даты начала договора
    IF NEW.start_date < CURRENT_DATE THEN
        RAISE EXCEPTION 'Дата начала договора должна быть не меньше текущей';
    END IF;

    -- Проверка отсутствия даты возврата автомобиля
    IF NEW.end_date IS NOT NULL THEN
        RAISE EXCEPTION 'Дата возврата не может быть определена изначально';
    END IF;

	 -- Проверка продолжительности
    IF NEW.duration <= 0 THEN
        RAISE EXCEPTION 'Продолжительность договора должна быть больше нуля';
    END IF;

    -- Установка стоимости договора
    NEW.total_cost := NEW.duration * 
	(SELECT models.rent_price FROM models 
	 JOIN autos ON models.name = autos.model 
	 WHERE autos.number = NEW.auto);

    RETURN NEW;
END;$$;
 +   DROP FUNCTION public.check_new_contract();
       public          postgres    false            �            1255    16471    get_expiry_date(date, integer)    FUNCTION     �   CREATE FUNCTION public.get_expiry_date(start_date date, duration integer) RETURNS date
    LANGUAGE plpgsql
    AS $$DECLARE
BEGIN
  RETURN start_date + duration;
END;$$;
 I   DROP FUNCTION public.get_expiry_date(start_date date, duration integer);
       public          postgres    false            �            1255    16484    make_report(character varying)    FUNCTION       CREATE FUNCTION public.make_report(brand_name character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$DECLARE
BEGIN
    -- Очистка таблицы report
    DELETE FROM public.report;

    -- Информация об автомобилях, находящихся в аренде 
    INSERT INTO public.report(number, year, color, mileage, tenant, start_date, end_date)
    SELECT
        a.number,
        a.year,
        a.color,
        a.mileage,
        cl.full_name,
        rc.start_date,
        get_expiry_date(rc.start_date, rc.duration)
    FROM
        public.autos AS a
        JOIN public.rent_contracts AS rc ON a.number = rc.auto
        JOIN public.clients AS cl ON rc.client = cl.id
        JOIN public.models AS m ON m.name = a.model
    WHERE
        m.brand = brand_name
        AND rc.end_date IS NULL;
	
	-- Информация об автомобилях, никогда не бывших в аренде
	INSERT INTO public.report (number, year, color, mileage)
    SELECT
        a.number,
        a.year,
        a.color,
        a.mileage
    FROM
        public.autos AS a
        JOIN public.models AS m ON m.name = a.model
    WHERE
        m.brand = brand_name
        AND a.number NOT IN (SELECT auto FROM public.rent_contracts);
	
	-- Информация об автомобилях, бывших в аренде ранее 
    INSERT INTO public.report (number, year, color, mileage, end_date, duration)
    SELECT
        a.number,
        a.year,
        a.color,
        a.mileage,
        MAX(rc.end_date),
        SUM(rc.duration)
    FROM
        public.autos AS a
        JOIN public.rent_contracts AS rc ON a.number = rc.auto
        JOIN public.models AS m ON m.name = a.model
    WHERE
        m.brand = brand_name
        AND rc.end_date >= CURRENT_DATE - INTERVAL '1 year'
        AND NOT EXISTS (
            SELECT *
            FROM public.rent_contracts AS rc2
            WHERE rc2.auto = a.number
            AND rc2.end_date IS NULL
        )
    GROUP BY
        a.number;
END;$$;
 @   DROP FUNCTION public.make_report(brand_name character varying);
       public          postgres    false            �            1255    16492    update_total_cost()    FUNCTION       CREATE FUNCTION public.update_total_cost() RETURNS trigger
    LANGUAGE plpgsql
    AS $$DECLARE
    price INTEGER;
    duration INTEGER;
BEGIN
	-- Проверка даты возврата
    IF NEW.end_date < NEW.start_date THEN
        RAISE EXCEPTION 'Дата возврата меньше даты заключения контракта';
    END IF;

	-- Определение стоимости аренды
    SELECT rent_price INTO price
    FROM models
    JOIN autos ON models.name = autos.model
    WHERE autos.number = NEW.auto;
	
	-- Определение стоимости по "реальной" продолжительности
    duration := NEW.end_date - NEW.start_date;
    NEW.total_cost := price * (duration);

    RETURN NEW;
END;$$;
 *   DROP FUNCTION public.update_total_cost();
       public          postgres    false            �            1259    16404    autos    TABLE     �   CREATE TABLE public.autos (
    number character(10) NOT NULL,
    year integer NOT NULL,
    color character(12) NOT NULL,
    condition character(12) DEFAULT 'undefined'::bpchar,
    mileage real NOT NULL,
    model character varying(30) NOT NULL
);
    DROP TABLE public.autos;
       public         heap    postgres    false            �            1259    16409    clients    TABLE     �   CREATE TABLE public.clients (
    id integer NOT NULL,
    full_name character varying(30) NOT NULL,
    license character(20),
    cert_date date,
    category character(3)
);
    DROP TABLE public.clients;
       public         heap    postgres    false            �            1259    16460 
   clients_id    SEQUENCE     s   CREATE SEQUENCE public.clients_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 !   DROP SEQUENCE public.clients_id;
       public          postgres    false    216            �           0    0 
   clients_id    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.clients_id OWNED BY public.clients.id;
          public          postgres    false    218            �            1259    16432    rent_contracts    TABLE     ;  CREATE TABLE public.rent_contracts (
    id integer NOT NULL,
    client integer NOT NULL,
    auto character(10) NOT NULL,
    start_date date NOT NULL,
    duration integer NOT NULL,
    end_date date,
    total_cost integer DEFAULT 0 NOT NULL,
    notes character varying(100) DEFAULT NULL::character varying
);
 "   DROP TABLE public.rent_contracts;
       public         heap    postgres    false            �            1259    16462    contract_id    SEQUENCE     t   CREATE SEQUENCE public.contract_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.contract_id;
       public          postgres    false    217            �           0    0    contract_id    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.contract_id OWNED BY public.rent_contracts.id;
          public          postgres    false    219            �            1259    16399    models    TABLE     �   CREATE TABLE public.models (
    name character varying(30) NOT NULL,
    brand character varying(30) NOT NULL,
    rent_price integer NOT NULL,
    capacity integer,
    body_type character(10)
);
    DROP TABLE public.models;
       public         heap    postgres    false            �            1259    16472    report    TABLE     �   CREATE TABLE public.report (
    number character(10) NOT NULL,
    year integer NOT NULL,
    color character(12) NOT NULL,
    mileage real NOT NULL,
    tenant character varying(30),
    start_date date,
    end_date date,
    duration integer
);
    DROP TABLE public.report;
       public         heap    postgres    false            "           2604    16461 
   clients id    DEFAULT     d   ALTER TABLE ONLY public.clients ALTER COLUMN id SET DEFAULT nextval('public.clients_id'::regclass);
 9   ALTER TABLE public.clients ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    216            #           2604    16501    rent_contracts id    DEFAULT     l   ALTER TABLE ONLY public.rent_contracts ALTER COLUMN id SET DEFAULT nextval('public.contract_id'::regclass);
 @   ALTER TABLE public.rent_contracts ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    219    217            �          0    16404    autos 
   TABLE DATA           O   COPY public.autos (number, year, color, condition, mileage, model) FROM stdin;
    public          postgres    false    215   c8       �          0    16409    clients 
   TABLE DATA           N   COPY public.clients (id, full_name, license, cert_date, category) FROM stdin;
    public          postgres    false    216   \9       �          0    16399    models 
   TABLE DATA           N   COPY public.models (name, brand, rent_price, capacity, body_type) FROM stdin;
    public          postgres    false    214   D:       �          0    16432    rent_contracts 
   TABLE DATA           m   COPY public.rent_contracts (id, client, auto, start_date, duration, end_date, total_cost, notes) FROM stdin;
    public          postgres    false    217   �:       �          0    16472    report 
   TABLE DATA           f   COPY public.report (number, year, color, mileage, tenant, start_date, end_date, duration) FROM stdin;
    public          postgres    false    220   �;       �           0    0 
   clients_id    SEQUENCE SET     9   SELECT pg_catalog.setval('public.clients_id', 1, false);
          public          postgres    false    218            �           0    0    contract_id    SEQUENCE SET     :   SELECT pg_catalog.setval('public.contract_id', 10, true);
          public          postgres    false    219            )           2606    16415    autos autos_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.autos
    ADD CONSTRAINT autos_pkey PRIMARY KEY (number);
 :   ALTER TABLE ONLY public.autos DROP CONSTRAINT autos_pkey;
       public            postgres    false    215            +           2606    16413    clients clients_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.clients DROP CONSTRAINT clients_pkey;
       public            postgres    false    216            '           2606    16403    models models_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.models
    ADD CONSTRAINT models_pkey PRIMARY KEY (name);
 <   ALTER TABLE ONLY public.models DROP CONSTRAINT models_pkey;
       public            postgres    false    214            -           2606    16437 "   rent_contracts rent_contracts_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.rent_contracts
    ADD CONSTRAINT rent_contracts_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.rent_contracts DROP CONSTRAINT rent_contracts_pkey;
       public            postgres    false    217            /           2606    16476    report report_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.report
    ADD CONSTRAINT report_pkey PRIMARY KEY (number);
 <   ALTER TABLE ONLY public.report DROP CONSTRAINT report_pkey;
       public            postgres    false    220            3           2620    16499 #   rent_contracts contracts_insert_new    TRIGGER     �   CREATE TRIGGER contracts_insert_new BEFORE INSERT ON public.rent_contracts FOR EACH ROW EXECUTE FUNCTION public.check_new_contract();
 <   DROP TRIGGER contracts_insert_new ON public.rent_contracts;
       public          postgres    false    234    217            4           2620    16500 (   rent_contracts contracts_update_end_year    TRIGGER     �   CREATE TRIGGER contracts_update_end_year BEFORE UPDATE OF end_date ON public.rent_contracts FOR EACH ROW EXECUTE FUNCTION public.update_total_cost();
 A   DROP TRIGGER contracts_update_end_year ON public.rent_contracts;
       public          postgres    false    217    235    217            0           2606    16454    autos fk_auto_model    FK CONSTRAINT     �   ALTER TABLE ONLY public.autos
    ADD CONSTRAINT fk_auto_model FOREIGN KEY (model) REFERENCES public.models(name) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 =   ALTER TABLE ONLY public.autos DROP CONSTRAINT fk_auto_model;
       public          postgres    false    215    214    3111            1           2606    16444    rent_contracts fk_contract_auto    FK CONSTRAINT     �   ALTER TABLE ONLY public.rent_contracts
    ADD CONSTRAINT fk_contract_auto FOREIGN KEY (auto) REFERENCES public.autos(number) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 I   ALTER TABLE ONLY public.rent_contracts DROP CONSTRAINT fk_contract_auto;
       public          postgres    false    3113    217    215            2           2606    16449 !   rent_contracts fk_contract_client    FK CONSTRAINT     �   ALTER TABLE ONLY public.rent_contracts
    ADD CONSTRAINT fk_contract_client FOREIGN KEY (client) REFERENCES public.clients(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 K   ALTER TABLE ONLY public.rent_contracts DROP CONSTRAINT fk_contract_client;
       public          postgres    false    217    3115    216            �   �   x����j�@@�g�b���n���$�K[{Qk��e1+���)���%�<.��(N�y�Sf`�2��c�����	$�VeS�,I�w���~,����B\Ԯ�e6��d#q2�izcx��2*���D�(�^� =�'׋�ΞeU����K �wjX�ŏ��`�:%��-�6��aR�f0ΕR�\����N�o���D7�P�n��G$�n�8|�M'#��$n�~�!�/+���      �   �   x�e�[
�0���*���݄+p1m�(����������I�h��͹3G<���q��C4x�|�>�G8��B����DjB��	+822�7��3A4�����q��␰�mf$��/�J^��Q�͑��݌'^ ����9&�S�B���9"ь���	�joS#������S��P&ܢ21�Fޞ-�.R˯�-���_p��<�=ߎ      �   c   x�ɯ�/ITpN�-��s8M8M9c���|�"L9����9Hȱ4%S�фDs�p��C�f����$�M1���b
�bn�,h��
��qqq d[%�      �   �   x�e�G� E��)r�)�ez�u���#c��N��ࣧ��((��	:��,��#��k�h�ː�r�UH�TUS�P�`��x��G�Ѯ5H	��9��q���.$���ϱЩd�t,����-5M�&�c������z��J���xB,=�l-m!���d�������C��@r=kW�0��y��ݭ��^7���5tν��M�      �   �   x����761U N#Cs��̜��"0�4300�0�;.6]l����N�s.l���bυ�@��.lj42�54�50D0�8c��"�M��a�[p:唦*@�	��?8�r��4������NLΆ��@��a �Ɛ�Ѐ+ 0�����Ȉӽ(�n�)�&S]#�&#�=... �AM     