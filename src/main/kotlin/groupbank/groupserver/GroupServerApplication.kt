package groupbank.groupserver

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class GroupServerApplication

fun main(args: Array<String>) {
    runApplication<GroupServerApplication>(*args)
}
