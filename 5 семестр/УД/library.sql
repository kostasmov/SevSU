PGDMP      3    	            |            library    16.1    16.3 -    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16398    library    DATABASE     {   CREATE DATABASE library WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE library;
                postgres    false            �            1259    16525    accounts    TABLE     �   CREATE TABLE public.accounts (
    login character varying(20) NOT NULL,
    password character varying(20) NOT NULL,
    role character varying NOT NULL,
    reader_id integer NOT NULL
);
    DROP TABLE public.accounts;
       public         heap    postgres    false            �           0    0    TABLE accounts    ACL     0   GRANT SELECT ON TABLE public.accounts TO staff;
          public          postgres    false    225            �            1259    16456    authors    TABLE     |   CREATE TABLE public.authors (
    id integer NOT NULL,
    first_name character varying,
    last_name character varying
);
    DROP TABLE public.authors;
       public         heap    postgres    false            �           0    0    TABLE authors    ACL     m   GRANT SELECT,INSERT,UPDATE ON TABLE public.authors TO staff;
GRANT SELECT ON TABLE public.authors TO reader;
          public          postgres    false    220            �            1259    16455    authors_id_seq    SEQUENCE     �   ALTER TABLE public.authors ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.authors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    220            �            1259    16463    book_author    TABLE     b   CREATE TABLE public.book_author (
    book_id integer NOT NULL,
    author_id integer NOT NULL
);
    DROP TABLE public.book_author;
       public         heap    postgres    false            �           0    0    TABLE book_author    ACL     u   GRANT SELECT,INSERT,DELETE ON TABLE public.book_author TO staff;
GRANT SELECT ON TABLE public.book_author TO reader;
          public          postgres    false    221            �            1259    16429    books    TABLE     �   CREATE TABLE public.books (
    id integer NOT NULL,
    title character varying NOT NULL,
    publisher character varying,
    book_year integer,
    amount integer DEFAULT 0 NOT NULL,
    type character varying
);
    DROP TABLE public.books;
       public         heap    postgres    false            �           0    0    TABLE books    ACL     i   GRANT SELECT,INSERT,UPDATE ON TABLE public.books TO staff;
GRANT SELECT ON TABLE public.books TO reader;
          public          postgres    false    216            �            1259    16438    issuance    TABLE     �   CREATE TABLE public.issuance (
    id integer NOT NULL,
    book_id integer NOT NULL,
    reader_id integer NOT NULL,
    book_date date,
    return_date date,
    status character varying DEFAULT 'pending'::character varying NOT NULL
);
    DROP TABLE public.issuance;
       public         heap    postgres    false            �           0    0    TABLE issuance    ACL     h   GRANT SELECT,UPDATE ON TABLE public.issuance TO staff;
GRANT INSERT ON TABLE public.issuance TO reader;
          public          postgres    false    218            �            1259    16513    books_amount    VIEW     �  CREATE VIEW public.books_amount AS
 SELECT books.id,
    books.title,
    books.amount AS total_amount,
    COALESCE(issued.amount, (0)::bigint) AS issued_amount,
    (books.amount - COALESCE(issued.amount, (0)::bigint)) AS available_amount
   FROM (public.books
     LEFT JOIN ( SELECT issuance.book_id,
            count(*) AS amount
           FROM public.issuance
          WHERE ((issuance.status)::text = 'issued'::text)
          GROUP BY issuance.book_id) issued ON ((books.id = issued.book_id)));
    DROP VIEW public.books_amount;
       public          postgres    false    216    218    218    216    216            �           0    0    TABLE books_amount    ACL     4   GRANT SELECT ON TABLE public.books_amount TO staff;
          public          postgres    false    224            �            1259    16428    books_id_seq    SEQUENCE     �   ALTER TABLE public.books ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.books_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    216            �            1259    16563 
   books_info    VIEW     A  CREATE VIEW public.books_info AS
 SELECT books.title,
    authors.first_name,
    authors.last_name,
    books.publisher,
    books.book_year,
    books.amount,
    books.type
   FROM ((public.books
     JOIN public.book_author ba ON ((ba.book_id = books.id)))
     JOIN public.authors ON ((authors.id = ba.author_id)));
    DROP VIEW public.books_info;
       public          postgres    false    220    221    221    220    216    216    216    220    216    216    216            �            1259    16437    issuance_id_seq    SEQUENCE     �   ALTER TABLE public.issuance ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.issuance_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    218            �            1259    16491    readers    TABLE     <  CREATE TABLE public.readers (
    id integer NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    group_code character varying,
    phone character varying,
    email character varying(256),
    fined boolean DEFAULT false NOT NULL,
    CONSTRAINT email CHECK (((email)::text ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'::text)),
    CONSTRAINT group_code CHECK (((group_code)::text ~* '[А-Я]{1,3}/б-[0-9]{2}-[0-9]-[а-я]{1,2}$'::text)),
    CONSTRAINT phone CHECK (((phone)::text ~ '^\+[0-9]{11,11}$'::text))
);
    DROP TABLE public.readers;
       public         heap    postgres    false            �           0    0    TABLE readers    ACL     6   GRANT SELECT,INSERT ON TABLE public.readers TO staff;
          public          postgres    false    223            �            1259    16490    readers_id_seq    SEQUENCE     �   ALTER TABLE public.readers ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.readers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    223            �          0    16525    accounts 
   TABLE DATA           D   COPY public.accounts (login, password, role, reader_id) FROM stdin;
    public          postgres    false    225   G6       �          0    16456    authors 
   TABLE DATA           <   COPY public.authors (id, first_name, last_name) FROM stdin;
    public          postgres    false    220   �6       �          0    16463    book_author 
   TABLE DATA           9   COPY public.book_author (book_id, author_id) FROM stdin;
    public          postgres    false    221   �7       �          0    16429    books 
   TABLE DATA           N   COPY public.books (id, title, publisher, book_year, amount, type) FROM stdin;
    public          postgres    false    216   8       �          0    16438    issuance 
   TABLE DATA           Z   COPY public.issuance (id, book_id, reader_id, book_date, return_date, status) FROM stdin;
    public          postgres    false    218   �9       �          0    16491    readers 
   TABLE DATA           ]   COPY public.readers (id, first_name, last_name, group_code, phone, email, fined) FROM stdin;
    public          postgres    false    223   :       �           0    0    authors_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.authors_id_seq', 15, true);
          public          postgres    false    219            �           0    0    books_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.books_id_seq', 11, true);
          public          postgres    false    215            �           0    0    issuance_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.issuance_id_seq', 12, true);
          public          postgres    false    217            �           0    0    readers_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.readers_id_seq', 25, true);
          public          postgres    false    222            J           2606    16533    accounts accounts_login_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_login_key UNIQUE (login);
 E   ALTER TABLE ONLY public.accounts DROP CONSTRAINT accounts_login_key;
       public            postgres    false    225            L           2606    16531    accounts accounts_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (reader_id);
 @   ALTER TABLE ONLY public.accounts DROP CONSTRAINT accounts_pkey;
       public            postgres    false    225            D           2606    16462    authors authors_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.authors
    ADD CONSTRAINT authors_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.authors DROP CONSTRAINT authors_pkey;
       public            postgres    false    220            F           2606    16467    book_author book_author_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.book_author
    ADD CONSTRAINT book_author_pkey PRIMARY KEY (book_id, author_id);
 F   ALTER TABLE ONLY public.book_author DROP CONSTRAINT book_author_pkey;
       public            postgres    false    221    221            @           2606    16436    books books_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.books DROP CONSTRAINT books_pkey;
       public            postgres    false    216            B           2606    16444    issuance issuance_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.issuance
    ADD CONSTRAINT issuance_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.issuance DROP CONSTRAINT issuance_pkey;
       public            postgres    false    218            H           2606    16501    readers reader_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY public.readers
    ADD CONSTRAINT reader_pkey PRIMARY KEY (id);
 =   ALTER TABLE ONLY public.readers DROP CONSTRAINT reader_pkey;
       public            postgres    false    223            Q           2606    16534     accounts accounts_reader_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_reader_id_fkey FOREIGN KEY (reader_id) REFERENCES public.readers(id) ON UPDATE CASCADE ON DELETE CASCADE;
 J   ALTER TABLE ONLY public.accounts DROP CONSTRAINT accounts_reader_id_fkey;
       public          postgres    false    223    4680    225            O           2606    16554 &   book_author book_author_author_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.book_author
    ADD CONSTRAINT book_author_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.authors(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 P   ALTER TABLE ONLY public.book_author DROP CONSTRAINT book_author_author_id_fkey;
       public          postgres    false    4676    221    220            P           2606    16549 $   book_author book_author_book_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.book_author
    ADD CONSTRAINT book_author_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.books(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 N   ALTER TABLE ONLY public.book_author DROP CONSTRAINT book_author_book_id_fkey;
       public          postgres    false    216    4672    221            M           2606    16539    issuance issuance_book_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.issuance
    ADD CONSTRAINT issuance_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.books(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 H   ALTER TABLE ONLY public.issuance DROP CONSTRAINT issuance_book_id_fkey;
       public          postgres    false    218    216    4672            N           2606    16544     issuance issuance_reader_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.issuance
    ADD CONSTRAINT issuance_reader_id_fkey FOREIGN KEY (reader_id) REFERENCES public.readers(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 J   ALTER TABLE ONLY public.issuance DROP CONSTRAINT issuance_reader_id_fkey;
       public          postgres    false    4680    218    223            �   S   x�KL����4 �D0ӌ��8��"br�EL�DL�"�H"�\y`!bd̕_��, ���,f
3D2�*�4��r��qqq 06*�      �   
  x�=P�N�0<{?a���>�I[ġ*q@P�!�c���8���1k#N����ΌwxA���#�VZ�=Ʌûn�aԹ�#�2!T+�L�t��et��_,���l���Gt����e9��~��l�,z$�:<q�];�s���ue"�=���C�<����v%��b焣�S�Hč��>$3Lg倖zn:ȥK]f=|�lC�$�I<p�#��!Kg����}΁��AR�'�,��Ӟ����f/!I����gE�gV[��7�ܞ��/Fq�      �   7   x�ƹ  ���TÁ���ׁ��2C��Iԧ���Ѯ�r�;W���V���Q�      �   o  x����N�@����O@�b��pG4��w�"1�7�ĸ2i
P��
g��3��L4.f23���K=�H�U[uT+,#�����S��k�e^�HT)r��_���V�ٰ��'�z��� �����)o�#��T��`���LS��5���4�Jq�knI��[$U����&�)@~�(4������#�̑�/i�Uk�z�*n��Ј4-$�˱:cd�e����m�؜��KTG0��w<b����`L%�H�%W+�X�c�^J��%�$,j�"x#��վ�����u��j��^(��I�gcez�p�jL����~S�+�ο#��Ű��(Ki3�36zI��}rѪ5����˲� tg�      �   �   x�e�K�0D��]�b�Ӟ�'`IT��*(��bؠx�d�̨(�E�I1����ĭ����%�$�q�1S��~@����EG#��%�*�X��xU�;?�9��̩T�7�����O�Uo˧�F!0ձ=k~���`7�      �   {  x�U��N�0Ư�^�YG��>7��/0������&� D#1&�ޛA$�<��y�12κ�k�������`���J������t�K����8?Ņɲ�e�N��|!4EP����(�\�he�=��8��q֪�;����\>�I������{�M��1~�(���F>ʑ�r�$��	~jEV����r�mz�':�H�T�PYT����{�ky��cd&;Xd���+��#�	/0X��b�Fqz���3���"�4��y��+���
� �u � �iay��>��Ѫ�����J�:��U�(�fj�<�Q��J��W%�Ώ3��V\��v�So�2W���Cm�M��&n���3���Ѿ�+�&�7f�A�L9c�?R�2�     