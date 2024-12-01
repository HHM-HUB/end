import dayjs from "dayjs"

import utc from "dayjs/plugin/utc"
dayjs.extend(utc)

export function formatUTC(UCT: string, format = "YYYY-MM-DD HH:mm:ss") {
  return dayjs.utc(UCT).utcOffset(8).format(format)
}
