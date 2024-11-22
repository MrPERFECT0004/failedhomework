import psycopg2
DATABASE_URL = "postgresql://foydalanuvchi_ismi:parol@server_manzili:port/ma'lumotlar_bazasi_ismi"
try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS avtomobillar (
            id SERIAL PRIMARY KEY,
            nomi VARCHAR(100) NOT NULL,
            model TEXT,
            yil INTEGER,
            narx NUMERIC(12, 2),
            mavjudmi BOOLEAN DEFAULT TRUE
        )
    """)



    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientlar (
            id SERIAL PRIMARY KEY,
            ism VARCHAR(50) NOT NULL,
            familiya VARCHAR(50),
            telefon CHAR(13),
            manzil TEXT
        )
    """)



    cur.execute("""
        CREATE TABLE IF NOT EXISTS buyurtmalar (
            id SERIAL PRIMARY KEY,
            avtomobil_id INTEGER REFERENCES avtomobillar(id),
            client_id INTEGER REFERENCES clientlar(id),
            sana DATE NOT NULL,
            umumiy_narx NUMERIC(12, 2)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS xodimlar (
            id SERIAL PRIMARY KEY,
            ism VARCHAR(50) NOT NULL,
            lavozim VARCHAR(50),
            maosh NUMERIC(10, 2)
        )
    """)



    cur.execute("ALTER TABLE clientlar ADD COLUMN email VARCHAR(100)")
    cur.execute("ALTER TABLE clientlar RENAME COLUMN ism TO toliq_ism") 
    cur.execute("ALTER TABLE clientlar RENAME TO mijozlar") 


   
    cur.execute("INSERT INTO avtomobillar (nomi, model, yil, narx) VALUES (%s, %s, %s, %s)", ("neksiya", "Chevrolet", 2023, 15000.00))
    cur.execute("INSERT INTO mijozlar (toliq_ism, familiya, telefon, manzil, email) VALUES (%s, %s, %s, %s, %s)", ("davronbek", "Nazarov", "+998991234567", "Toshkent", "davron@gmail.com"))
    cur.execute("INSERT INTO buyurtmalar (avtomobil_id, client_id, sana, umumiy_narx) VALUES (%s, %s, %s, %s)", (1, 1, "2024-03-08", 15000.00))
    cur.execute("INSERT INTO xodimlar (ism, lavozim, maosh) VALUES (%s, %s, %s)", ("Muhammadjon", "Menejment", 2000.00))


    conn.commit()

    cur.execute("UPDATE xodimlar SET ism = 'Olim' WHERE id = 1")
    cur.execute("UPDATE xodimlar SET ism = 'Jamshid' WHERE id = 2")
    conn.commit()

    cur.execute("DELETE FROM xodimlar WHERE id = 1")
    conn.commit()

    cur.execute("SELECT * FROM avtomobillar")
    print("Avtomobillar jadvali:")
    for row in cur:
        print(row)



    cur.execute("SELECT * FROM mijozlar")
    print("\nMijozlar jadvali:")
    for row in cur:
        print(row)


    cur.execute("SELECT * FROM buyurtmalar")
    print("\nBuyurtmalar jadvali:")
    for row in cur:
        print(row)


    cur.execute("SELECT * FROM xodimlar")
    print("\nXodimlar jadvali:")
    for row in cur:
        print(row)

except psycopg2.Error as e:
    print(f"Xatolik yuz berdi: {e}")
finally:
    if conn:
        cur.close()
        conn.close()
