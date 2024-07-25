import { Pool } from 'pg';

const pool = new Pool({
  user: 'ltuser',
  host: 'localhost',
  database: 'langtrace',
  password: 'ltpasswd',
  port: 5432,
});

async function queryDatabase() {
    try {
      const client = await pool.connect();
      const res = await client.query('SELECT * FROM "Data"; ');
      console.log(res.rows[0]);
      client.release();
    } catch (err) {
      console.error(err);
    }
  }
  
  queryDatabase();