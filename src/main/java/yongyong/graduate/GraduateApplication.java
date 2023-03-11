package yongyong.graduate;

import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import yongyong.graduate.common.util.TodayUtil;

import javax.annotation.PostConstruct;
import java.util.*;

@Slf4j
//@SuppressWarnings("unused")
@SpringBootApplication
public class GraduateApplication {
	@PostConstruct
	public void started() {
		TimeZone.setDefault(TimeZone.getTimeZone("Asia/Seoul"));
	}

	public static void main(String[] args) {
		log.info("[GraduateApplication] today : {}", TodayUtil.getToday()); //초기 날짜 확인
		SpringApplication.run(GraduateApplication.class, args);
	}
}

