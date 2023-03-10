package yongyong.graduate.common;

import org.springframework.core.annotation.AliasFor;

import java.lang.annotation.*;

@Inherited
@Documented
@Target({ ElementType.TYPE })
@Retention(RetentionPolicy.RUNTIME)
public @interface TodayDoc {

    String collection = Today.lastUpdated + "_doc";

    @AliasFor("collection")
    String value() default collection;

    @AliasFor("value")
    String collection() default collection;
}
