CREATE TABLE PONTO_DE_TROCA (
        CEP             CHAR(8)         NOT NULL,            -- Cep no formato XXXXXXXX, sem travessão no meio
        NUMERO          NUMBER          NOT NULL,            -- Numero do endereço
        CIDADE          VARCHAR(30)     NOT NULL,            -- Nome da cidade
        RUA             VARCHAR(30)     NOT NULL,            -- Nome da rua
        NOME            VARCHAR(30)             ,            -- Nome do ponto de troca
        HOR_ABERTURA    DATE,                                -- Horario de abertura
        HOR_FECHA       DATE,                                -- Horario de fechamento
        
        CONSTRAINT      PK_PONTO_TROCA      PRIMARY KEY     (CEP, NUMERO, CIDADE, RUA)          -- Chave primaria da tabela
);

CREATE TABLE EVENTO(
        CEP             CHAR(8)         NOT NULL,            -- Cep no formato XXXXXXXX, sem travessão no meio
        NUMERO          NUMBER          NOT NULL,            -- Numero do endereço
        CIDADE          VARCHAR(30)     NOT NULL,            -- Nome da cidade
        RUA             VARCHAR(30)     NOT NULL,            -- Nome da rua
        DATA_EVENTO     DATE            NOT NULL,            -- Data do evento
        ID_EVENTO       NUMBER GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
        NOME            VARCHAR(30)     NOT NULL,            -- Nome do evento
        
        CONSTRAINT      PK_EVENTO           PRIMARY KEY     (ID_EVENTO),
        CONSTRAINT      SEC_KEY             UNIQUE          (CEP, NUMERO, CIDADE, RUA),
        CONSTRAINT      FK1_EVENTO          FOREIGN KEY     (CEP, NUMERO, CIDADE, RUA)      REFERENCES      PONTO_DE_TROCA(CEP, NUMERO, CIDADE, RUA)    ON DELETE CASCADE
        
);

CREATE TABLE PESSOA (
        USERNAME        VARCHAR(30)     NOT NULL,
        CPF             CHAR(11),
        NOME            VARCHAR(30),
        DATA_NASC       DATE,
        CEP             CHAR(8),            -- Cep no formato XXXXXXXX, sem travessão no meio
        NUMERO          NUMBER,            -- Numero do endereço
        CIDADE          VARCHAR(30),            -- Nome da cidade
        RUA             VARCHAR(30),            -- Nome da rua
        
        CONSTRAINT      PK_PESSOA       PRIMARY KEY (USERNAME),
        CONSTRAINT      UNI1_PESSOA     UNIQUE (CPF)
        

);

CREATE TABLE COLECIONADOR (
        USERNAME        VARCHAR(30)     NOT NULL,
        
        CONSTRAINT      PK_COLECIONADOR PRIMARY KEY     (USERNAME),
        CONSTRAINT      FK1_COLECIONADOR    FOREIGN KEY (USERNAME) REFERENCES PESSOA (USERNAME)
);

CREATE TABLE FUNCAO (
        USERNAME        VARCHAR(30)     NOT NULL,
        FUNCAO          CHAR(13)        NOT NULL,
        
        CONSTRAINT      PK_FUNCAO       PRIMARY KEY (USERNAME, FUNCAO),
        CONSTRAINT      FK1_FUNCAO      FOREIGN KEY (USERNAME) REFERENCES PESSOA(USERNAME),
        CONSTRAINT      CHECK_FUNC      CHECK (FUNCAO IN ('DONO DE BANCA','ORGANIZADOR','COLECIONADOR'))
);

CREATE TABLE ORGANIZADOR (
        USERNAME        VARCHAR(30)     NOT NULL,
        
        CONSTRAINT      PK_ORGANIZADOR      PRIMARY KEY     (USERNAME),
        CONSTRAINT      FK1_ORGANIZADOR     FOREIGN KEY (USERNAME) REFERENCES PESSOA (USERNAME)
);

CREATE TABLE DONO_BANCA (
        USERNAME        VARCHAR(30)     NOT NULL,
        COD_ID          NUMBER(10)      NOT NULL,
        
        CONSTRAINT      PK_DONO_BANCA       PRIMARY KEY     (USERNAME),
        CONSTRAINT      FK1_DONO_BANCA      FOREIGN KEY (USERNAME) REFERENCES PESSOA (USERNAME)
);

CREATE TABLE BANCA(
        CEP             CHAR(8)         NOT NULL,            -- Cep no formato XXXXXXXX, sem travessão no meio
        NUMERO          NUMBER          NOT NULL,            -- Numero do endereço
        CIDADE          VARCHAR(30)     NOT NULL,            -- Nome da cidade
        RUA             VARCHAR(30)     NOT NULL,            -- Nome da rua
        CNPJ            CHAR(14)        NOT NULL,
        USER_DONO       VARCHAR(30),
        
        CONSTRAINT      PK_BANCA           PRIMARY KEY (CNPJ),
        CONSTRAINT      FK1_BANCA          FOREIGN KEY     (CEP, NUMERO, CIDADE, RUA)      REFERENCES      PONTO_DE_TROCA(CEP, NUMERO, CIDADE, RUA)    ON DELETE CASCADE,
        CONSTRAINT      FK2_BANCA          FOREIGN KEY     (USER_DONO) REFERENCES DONO_BANCA(USERNAME)
);

CREATE TABLE COMPRA(
        USER_COMPRADOR      VARCHAR(30),
        NOTA_FISCAL         CHAR(20)        NOT NULL,
        CNPJ                CHAR(14)        NOT NULL,
        
        CONSTRAINT          PK_COMPRA       PRIMARY KEY (NOTA_FISCAL),
        CONSTRAINT          FK1_COMPRA      FOREIGN KEY (USER_COMPRADOR) REFERENCES COLECIONADOR(USERNAME) ON DELETE CASCADE,
        CONSTRAINT          FK_2_COMPRA     FOREIGN KEY (CNPJ) REFERENCES BANCA (CNPJ)
);

CREATE TABLE DIVULGA(
        USER_DIVULGADOR     VARCHAR(30)     NOT NULL,
        ID_EVENTO           NUMBER          NOT NULL,
        
        CONSTRAINT          PK_DIVULGA      PRIMARY KEY (USER_DIVULGADOR, ID_EVENTO),
        CONSTRAINT          FK1_DIVULGA     FOREIGN KEY (USER_DIVULGADOR) REFERENCES PESSOA(USERNAME) ON DELETE CASCADE,
        CONSTRAINT          FK2_DIVULGA     FOREIGN KEY (ID_EVENTO) REFERENCES EVENTO(ID_EVENTO) ON DELETE CASCADE
);

CREATE TABLE ORG_EVENTO(
        ID_EVENTO       NUMBER          NOT NULL,
        USER_ORG        VARCHAR(30)     NOT NULL,
        NOME_TIME       VARCHAR(50)     NOT NULL,
        
        CONSTRAINT          PK_ORG_EVENTO      PRIMARY KEY (ID_EVENTO),
        CONSTRAINT          FK1_ORG_EVENTO     FOREIGN KEY (USER_ORG) REFERENCES ORGANIZADOR(USERNAME) ON DELETE CASCADE,
        CONSTRAINT          FK2_ORG_EVENTO     FOREIGN KEY (ID_EVENTO) REFERENCES EVENTO(ID_EVENTO) ON DELETE CASCADE
);

CREATE TABLE VOLUNTARIA(
        USER_VOLUNTARIO     VARCHAR(30)     NOT NULL,
        ID_EVENTO           NUMBER          NOT NULL,
        
        CONSTRAINT          PK_VOLUNTARIA      PRIMARY KEY (USER_VOLUNTARIO, ID_EVENTO),
        CONSTRAINT          FK1_VOLUNTARIA     FOREIGN KEY (USER_VOLUNTARIO) REFERENCES PESSOA(USERNAME) ON DELETE CASCADE,
        CONSTRAINT          FK2_VOLUNTARIA     FOREIGN KEY (ID_EVENTO) REFERENCES ORG_EVENTO(ID_EVENTO) ON DELETE CASCADE
);

CREATE TABLE PARTICIPA(
        USER_PARTICIPANTE     VARCHAR(30)     NOT NULL,
        ID_EVENTO           NUMBER          NOT NULL,
        
        CONSTRAINT          PK_PARTICIPA      PRIMARY KEY (USER_PARTICIPANTE, ID_EVENTO),
        CONSTRAINT          FK1_PARTICIPA     FOREIGN KEY (USER_PARTICIPANTE) REFERENCES COLECIONADOR(USERNAME) ON DELETE CASCADE,
        CONSTRAINT          FK2_PARTICIPA     FOREIGN KEY (ID_EVENTO) REFERENCES EVENTO(ID_EVENTO) ON DELETE CASCADE
);

CREATE TABLE ALBUM(
        ID_ALBUM            VARCHAR(10)         NOT NULL,
        COLECAO             VARCHAR(30)         NOT NULL,
        
        CONSTRAINT          PK_ALBUM            PRIMARY KEY (ID_ALBUM)
);

CREATE TABLE FIGURINHA(
        COD_FIGURINHA       VARCHAR(10)     NOT NULL,
        ID_ALBUM            VARCHAR(10)     NOT NULL,
        TIPO                VARCHAR(20)     NOT NULL,
        
        CONSTRAINT          PK_FIGURINHA        PRIMARY KEY (COD_FIGURINHA, ID_ALBUM),
        CONSTRAINT          FK1_FIGURINHA       FOREIGN KEY (ID_ALBUM) REFERENCES ALBUM(ID_ALBUM)
);

CREATE TABLE ALBUM_COLECIONADOR(
        USERNAME        VARCHAR(30)     NOT NULL,
        ID_ALBUM        VARCHAR(10)     NOT NULL,
        ID_INC          NUMBER GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
        
        CONSTRAINT          PK_ALBUM_COLECIONADOR       PRIMARY KEY (ID_ALBUM, ID_INC, USERNAME),
        CONSTRAINT          FK1_ALBUM_COLECIONADOR      FOREIGN KEY (ID_ALBUM) REFERENCES ALBUM(ID_ALBUM),
        CONSTRAINT          FK2_ALBUM_COLECIONADOR      FOREIGN KEY (USERNAME) REFERENCES COLECIONADOR(USERNAME)
);

CREATE TABLE FIGURINHA_COLECIONADOR(
        USERNAME        VARCHAR(30)     NOT NULL,
        COD_FIGURINHA   VARCHAR(10)     NOT NULL,
        ID_ALBUM        VARCHAR(10)     NOT NULL,
        ID_FIG_COLECIONADOR VARCHAR(20) NOT NULL,
        QUANT           NUMBER(2)       NOT NULL,
        
        CONSTRAINT      PK_FIG_COLECIONADOR PRIMARY KEY (ID_FIG_COLECIONADOR),
        CONSTRAINT      UNIQ_FIG_COLECIONADOR   UNIQUE(USERNAME, COD_FIGURINHA, ID_ALBUM),
        CONSTRAINT      FK1_FIG_COLECIONADOR    FOREIGN KEY (USERNAME) REFERENCES COLECIONADOR(USERNAME),
        CONSTRAINT      FK2_FIG_COLECIONADOR    FOREIGN KEY (COD_FIGURINHA, ID_ALBUM) REFERENCES FIGURINHA(COD_FIGURINHA, ID_ALBUM)
        
);

CREATE TABLE FIGURINHA_ALBUM(
    USERNAME        VARCHAR(30)     NOT NULL,
    ID_ALBUM        VARCHAR(10)     NOT NULL,
    ID_INC          NUMBER          NOT NULL,
    ID_FIGURINHA    VARCHAR(20)     NOT NULL,
    
    CONSTRAINT      PK_FIG_ALBUM        PRIMARY KEY (USERNAME, ID_ALBUM, ID_INC, ID_FIGURINHA),
    CONSTRAINT      FK1_FIG_ALBUM       FOREIGN KEY (USERNAME, ID_ALBUM, ID_INC) REFERENCES ALBUM_COLECIONADOR(USERNAME, ID_ALBUM, ID_INC),
    CONSTRAINT      FK2_FIG_ALBUM       FOREIGN KEY (ID_FIGURINHA) REFERENCES FIGURINHA_COLECIONADOR(ID_FIG_COLECIONADOR)
);

CREATE TABLE TRANSACAO(
        ID_TRANSACAO        NUMBER GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
        USER1           VARCHAR(30)     NOT NULL,
        USER2           VARCHAR(30)     NOT NULL,
        
        CONSTRAINT      PK_TRANSACAO        PRIMARY KEY (ID_TRANSACAO),
        CONSTRAINT      FK1_TRANSACAO       FOREIGN KEY (USER1) REFERENCES COLECIONADOR(USERNAME),
        CONSTRAINT      FK2_TRANSACAO       FOREIGN KEY (USER2) REFERENCES COLECIONADOR(USERNAME)
);

CREATE TABLE TROCA(
        ID_TRANSACAO        NUMBER      NOT NULL,
        DATA                DATE        NOT NULL,
        CEP             CHAR(8)         NOT NULL,            -- Cep no formato XXXXXXXX, sem travessão no meio
        NUMERO          NUMBER          NOT NULL,            -- Numero do endereço
        CIDADE          VARCHAR(30)     NOT NULL,            -- Nome da cidade
        RUA             VARCHAR(30)     NOT NULL,            -- Nome da rua
        
        CONSTRAINT      PK_TROCA        PRIMARY KEY (ID_TRANSACAO, DATA),
        CONSTRAINT      FK1_TROCA       FOREIGN KEY     (CEP, NUMERO, CIDADE, RUA)      REFERENCES      PONTO_DE_TROCA(CEP, NUMERO, CIDADE, RUA)    ON DELETE CASCADE
        
);

CREATE TABLE FIG_TROCA(
        ID_TRANSACAO        NUMBER      NOT NULL,
        DATA                DATE        NOT NULL,
        ID_FIG              VARCHAR(20) NOT NULL,
        QUANT               NUMBER(2)   NOT NULL,
        
        CONSTRAINT          PK_FIG_TROCA    PRIMARY KEY (ID_TRANSACAO, DATA, ID_FIG),
        CONSTRAINT          FK1_FIG_TROCA   FOREIGN KEY (ID_TRANSACAO, DATA) REFERENCES TROCA(ID_TRANSACAO, DATA),
        CONSTRAINT          FK2_FIG_TROCA   FOREIGN KEY (ID_FIG) REFERENCES FIGURINHA_COLECIONADOR(ID_FIG_COLECIONADOR)
);