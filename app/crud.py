import ipaddress
from typing import List
from .database import get_db_connection
from .models import IPAddress
import logging
from sqlite3 import Error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_ip_address(ip_str: str) -> bool:
    try:
        if ':' in ip_str:
            ip, port = ip_str.split(':')
            if not port.isdigit():
                return False
            ipaddress.ip_address(ip)
        else:
            ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False


def create_ip_address(ip_address: str) -> bool:
    if not validate_ip_address(ip_address):
        logger.error(f"Invalid IP address format: {ip_address}")
        return False

    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return False

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ip_addresses (ip_address) 
            VALUES (?)
            ON CONFLICT(ip_address) DO NOTHING
        """, (ip_address,))
        conn.commit()
        return cursor.rowcount > 0

    except Error as e:
        logger.error(f"Database error in create_ip_address: {e}")
        return False
    finally:
        if conn:
            conn.close()


def get_all_ip_addresses() -> List[IPAddress]:
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        cursor.execute("SELECT id, ip_address FROM ip_addresses")
        rows = cursor.fetchall()
        return [IPAddress(id=row[0], ip_address=row[1]) for row in rows]

    except Error as e:
        logger.error(f"Database error in get_all_ip_addresses: {e}")
        return []
    finally:
        if conn:
            conn.close()


def delete_ip_address(ip_address: str) -> bool:
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return False

        cursor = conn.cursor()
        cursor.execute("DELETE FROM ip_addresses WHERE ip_address = ?", (ip_address,))
        conn.commit()
        return cursor.rowcount > 0

    except Error as e:
        logger.error(f"Database error in delete_ip_address: {e}")
        return False
    finally:
        if conn:
            conn.close()


def search_ip_addresses(search_term: str) -> List[IPAddress]:
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, ip_address 
            FROM ip_addresses 
            WHERE ip_address LIKE ?
        """, (f"%{search_term}%",))
        rows = cursor.fetchall()
        return [IPAddress(id=row[0], ip_address=row[1]) for row in rows]

    except Error as e:
        logger.error(f"Database error in search_ip_addresses: {e}")
        return []
    finally:
        if conn:
            conn.close()


def import_from_file(file_path: str) -> bool:
    try:
        with open(file_path, 'r') as file:
            ip_addresses = [line.strip() for line in file if line.strip() and validate_ip_address(line.strip())]

        if not ip_addresses:
            return False

        conn = get_db_connection()
        if not conn:
            return False

        cursor = conn.cursor()
        cursor.executemany(
            "INSERT OR IGNORE INTO ip_addresses (ip_address) VALUES (?)",
            [(ip,) for ip in ip_addresses]
        )
        conn.commit()
        return True

    except Exception as e:
        logger.error(f"Error in import_from_file: {e}")
        return False
    finally:
        if conn:
            conn.close()


def export_to_file(file_path: str) -> bool:
    try:
        ip_addresses = get_all_ip_addresses()
        with open(file_path, 'w') as file:
            for ip in ip_addresses:
                file.write(f"{ip.ip_address}\n")
        return True
    except Exception as e:
        logger.error(f"Error in export_to_file: {e}")
        return False