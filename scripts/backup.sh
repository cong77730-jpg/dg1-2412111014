if [ $# -eq 0 ] || [ ! -d "$1" ]; then
    echo "Loi: Tham so thu muc khong hop le."
    exit 1
fi

SOURCE_DIR="$1"
DIR_NAME=$(basename "$SOURCE_DIR")
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="$HOME/backup"
BACKUP_FILE="${BACKUP_DIR}/${DIR_NAME}_${TIMESTAMP}.tar.gz"

mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_FILE" -C "$(dirname "$SOURCE_DIR")" "$DIR_NAME"

if [ $? -eq 0 ]; then
    LOG_FILE="$(dirname "$0")/../logs/backup.log"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] Backup thanh cong: $BACKUP_FILE" >> "$LOG_FILE"
    echo "Sao luu thanh cong: $BACKUP_FILE"
    exit 0
else
    echo "Loi trong qua trinh nen."
    exit 2
fi
