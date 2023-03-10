package yongyong.graduate.common;

import java.lang.annotation.*;

@Inherited
@Documented
@Target({ElementType.FIELD, ElementType.LOCAL_VARIABLE, ElementType.TYPE })
@Retention(RetentionPolicy.RUNTIME)
public @interface Today {
    String lastUpdated = "2023-03-09";
    String value() default lastUpdated;

}
