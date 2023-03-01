package yongyong.graduate.config;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

@Configuration
// package 달라야함
@EnableMongoRepositories(basePackages = {"yongyong.graduate.docDomain"},
mongoTemplateRef = Db2Config.MONGO_TEMPLATE)
public class Db2Config {
    protected static final String MONGO_TEMPLATE = "db2MongoTemplate";
}
