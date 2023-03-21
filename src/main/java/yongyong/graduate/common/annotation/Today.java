package yongyong.graduate.common.annotation;

import java.lang.annotation.*;

@Inherited
@Documented
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface Today {
    String lastUpdated = "2023-03-21";
    String value() default lastUpdated;

}
